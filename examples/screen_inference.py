"""Real-time YOLO inference over a region of the screen.

Captures a screen region with ``pyautogui``, runs an Ultralytics checkpoint and
draws the detections with OpenCV.

Usage
-----
    python examples/screen_inference.py --model weights/ow2-yolo11m.pt

    # Capture the top-left 1280x720 region at 300 FPS-independent loop
    python examples/screen_inference.py --model weights/cs2_yolov10s.pt \
        --region 1280x720+0+0 --conf 0.35

Press ``q`` in the preview window to quit.
"""

from __future__ import annotations

import argparse
import time

import cv2
import numpy as np

BOX_COLOR = (34, 211, 238)      # cyan (BGR)
TEXT_COLOR = (248, 250, 252)    # near-white (BGR)
FONT = cv2.FONT_HERSHEY_SIMPLEX


def parse_region(value: str) -> tuple[int, int, int, int]:
    """Parse a WxH+X+Y screen region."""
    try:
        size, x, y = value.lower().split("+")
        width, height = size.split("x")
        return int(x), int(y), int(width), int(height)
    except (ValueError, AttributeError) as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid region {value!r}. Expected WxH+X+Y, e.g. 1280x720+0+0"
        ) from exc


def default_region(screen_width: int, screen_height: int) -> tuple[int, int, int, int]:
    """640x640 region centered on the primary screen."""
    size = 640
    return (screen_width - size) // 2, (screen_height - size) // 2, size, size


def draw_detections(frame: np.ndarray, result, names: dict[int, str]) -> np.ndarray:
    for box in result.boxes:
        x1, y1, x2, y2 = (int(v) for v in box.xyxy[0].tolist())
        confidence = float(box.conf[0])
        class_name = names.get(int(box.cls[0]), str(int(box.cls[0])))

        cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
        label = f"{class_name} {confidence:.2f}"
        (text_width, text_height), baseline = cv2.getTextSize(label, FONT, 0.5, 1)
        cv2.rectangle(
            frame,
            (x1, max(0, y1 - text_height - baseline - 4)),
            (x1 + text_width + 4, y1),
            BOX_COLOR,
            -1,
        )
        cv2.putText(
            frame,
            label,
            (x1 + 2, y1 - baseline - 2),
            FONT,
            0.5,
            (4, 18, 31),
            1,
            cv2.LINE_AA,
        )
    return frame


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Path or name of the YOLO checkpoint")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument(
        "--region",
        type=parse_region,
        default=None,
        help="Screen region as WxH+X+Y (default: 640x640 centered)",
    )
    parser.add_argument(
        "--classes",
        nargs="*",
        type=int,
        default=None,
        help="Optional class IDs to keep (default: all)",
    )
    parser.add_argument("--max-det", type=int, default=50, help="Maximum detections per frame")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        import pyautogui
        from ultralytics import YOLO
    except ModuleNotFoundError as exc:
        raise SystemExit(
            f"Missing dependency '{exc.name}'. Install the example requirements with:\n"
            "  pip install -r requirements.txt"
        ) from exc

    region = args.region or default_region(*pyautogui.size())

    model = YOLO(args.model)
    print(f"Model: {args.model}")
    print(f"Region: {region[2]}x{region[3]}+{region[0]}+{region[1]}")
    print("Press 'q' in the preview window to quit.")

    previous = time.perf_counter()
    fps = 0.0

    while True:
        screenshot = pyautogui.screenshot(region=region)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        results = model.predict(
            frame,
            conf=args.conf,
            classes=args.classes,
            max_det=args.max_det,
            verbose=False,
        )
        frame = draw_detections(frame, results[0], model.names)

        now = time.perf_counter()
        instant_fps = 1.0 / max(now - previous, 1e-6)
        fps = instant_fps if fps == 0.0 else 0.9 * fps + 0.1 * instant_fps
        previous = now

        cv2.putText(
            frame,
            f"{fps:.1f} FPS",
            (8, 22),
            FONT,
            0.6,
            TEXT_COLOR,
            1,
            cv2.LINE_AA,
        )
        cv2.imshow("YOLO screen inference", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
