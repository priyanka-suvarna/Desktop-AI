import cv2
import numpy as np
import pyautogui
import time
from datetime import datetime

def start_screen_recording(output_path=None, fps=30):
    # Generate default filename with timestamp if none provided
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"screen_recording_{timestamp}.mp4"
    
    # Ensure output path ends with proper video extension
    if not output_path.lower().endswith(('.mp4', '.avi')):
        output_path += '.mp4'
    
    # Get screen size and adjust for potential scaling issues
    screen_size = pyautogui.size()
    width, height = screen_size
    
    try:
        # Use more efficient codec (mp4v for .mp4, xvid for .avi)
        codec = 'mp4v' if output_path.lower().endswith('.mp4') else 'xvid'
        out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*codec),
            fps,
            (width, height)
        )
        
        if not out.isOpened():
            raise Exception("Failed to create video writer")

        print(f"Screen recording started. Output: {output_path}")
        print("Press 'q' to stop recording")
        
        frames_captured = 0
        start_time = time.time()
        
        while True:
            try:
                # Capture screenshot with error handling
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Write frame
                out.write(frame)
                frames_captured += 1
                
                # Show recording preview (scaled down for performance)
                preview_frame = cv2.resize(frame, (width // 2, height // 2))
                cv2.imshow("Recording Preview", preview_frame)
                
                # Check for 'q' press with proper delay
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
            except Exception as e:
                print(f"Error capturing frame: {str(e)}")
                continue
            
    except Exception as e:
        print(f"Recording failed: {str(e)}")
        return False
        
    finally:
        # Cleanup
        if 'out' in locals():
            out.release()
        cv2.destroyAllWindows()
        
        # Display recording statistics
        if frames_captured > 0:
            duration = time.time() - start_time
            actual_fps = frames_captured / duration
            print(f"\nRecording stopped")
            print(f"Duration: {duration:.2f} seconds")
            print(f"Frames captured: {frames_captured}")
            print(f"Actual FPS: {actual_fps:.2f}")
            print(f"Output saved to: {output_path}")
        
        return True

if __name__ == "__main__":
    start_screen_recording()
