"""
MANET Simulator - OMNeT++ / INETMANET-3.x Controller

Main entry point for the OMNeT++ controller GUI.
"""

import tkinter as tk
import sys
from gui import MANETSimulatorGUI

def main():
    """Main function to run the MANET simulator GUI"""
    try:
        # Run GUI application
        root = tk.Tk()
        app = MANETSimulatorGUI(root)
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            print("Application interrupted by user")
        except Exception as e:
            print("Application error:", e)
            raise
            
    except ImportError as e:
        print("Error importing modules:", e)
        print("Make sure all required modules are in the same directory.")
        return 1
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
