from ultralytics import YOLO
import cv2
from pathlib import Path
from core.config import CONFIDENCE_THRESHOLD, IMAGE_SIZE, get_model_path
import sys



class SartoFlowDetector:
    def __init__(self, confidence=CONFIDENCE_THRESHOLD):
        model_path = get_model_path()
        print("start getting model from", model_path)

        self.model = YOLO(str(model_path))
        self.confidence = confidence

        print("model created")

    def detect(self, path_image):
        path_image = Path(path_image)
        print("this is path image", path_image)

        if not path_image.exists():
            raise FileNotFoundError(f"Image not found at {path_image}")

        results = self.model(path_image, conf=self.confidence, imgsz=IMAGE_SIZE, verbose=False)
        return results[0]

    def draw_boxes(self, image_path, results, output_path=None):
        """
        Draw bounding boxes on image and save it
        Returns path to saved image
        """
        image_path = Path(image_path)
        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError(f"Could not read image: {image_path}")

        boxes = results.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            class_id   = int(box.cls[0])
            confidence = float(box.conf[0])
            label      = results.names[class_id]

            # Draw box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label background
            text       = f"{label} {confidence:.2f}"
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(image, (x1, y1 - th - 8), (x1 + tw, y1), (0, 255, 0), -1)

            # Draw label text
            cv2.putText(image, text, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # Save result
        if output_path is None:
            output_path = image_path.parent / f"{image_path.stem}_result{image_path.suffix}"

        cv2.imwrite(str(output_path), image)
        return output_path

    def get_summary(self, results):
        """
        Return a clean dict summary of detections
        """
        detections = []
        for box in results.boxes:
            class_id   = int(box.cls[0])
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            detections.append({
                "label":      results.names[class_id],
                "confidence": round(confidence, 3),
                "box": {
                    "x1": int(x1), "y1": int(y1),
                    "x2": int(x2), "y2": int(y2)
                }
            })

        return {
            "total":      len(detections),
            "detections": detections
        }


# ─── Quick standalone test ──────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  FlowGuard - Detector Test")
    print("=" * 50)

    # Accept image path as argument or use a default
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
    else:
        # create a path inside project
        base_dir = get_model_path().parent.parent
        test_image = str(base_dir / "sample" / "test" / "test.jpg")

        Path(test_image).parent.mkdir(parents=True, exist_ok=True)

        print("No image provided — downloading sample image...")

        import urllib.request
        urllib.request.urlretrieve(
            "https://ultralytics.com/images/bus.jpg",
            test_image
        )

        print(f"Downloaded to: {test_image}")

    # Run detection
    detector = SartoFlowDetector()
    results  = detector.detect(test_image)
    summary  = detector.get_summary(results)
    output   = detector.draw_boxes(test_image, results)

    # Print results
    print(f"\n✅ Detection complete!")
    print(f"   Objects found : {summary['total']}")
    print()

    for i, d in enumerate(summary['detections'], 1):
        print(f"   {i}. {d['label']:<15} confidence: {d['confidence']}")

    print(f"\n📁 Result image saved to:")
    print(f"   {output}")
    print()
    print("Open the result image to see the boxes drawn!")
