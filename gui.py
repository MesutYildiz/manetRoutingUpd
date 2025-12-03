"""
MANET Simulator GUI - OMNeT++ / INETMANET-3.x Controller

Simplified OMNeT++ Control Panel.
Old Python simulator completely removed.
Only manages OMNeT++ and displays results.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging

# Import our manager module
# If you get an error here, make sure omnet_manager.py exists
from omnet_manager import OmnetManager

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MANETSimulatorGUI:
    """
    Simplified OMNeT++ Control Panel.
    Old Python simulator completely removed.
    Only manages OMNeT++ and displays results.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("MANET Simulator - OMNeT++ Controller")
        
        # Window size and position
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Initialize OMNeT++ Manager
        try:
            self.omnet_manager = OmnetManager()
            logger.info("OMNeT++ Manager successfully initialized")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize OMNeT++ Manager:\n{str(e)}")
            self.omnet_manager = None

        # Create GUI widgets
        self.create_widgets()

    def create_widgets(self):
        # --- Main Frame ---
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Title ---
        title_label = ttk.Label(
            main_frame, 
            text="OMNeT++ / INETMANET Simulation Control", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # --- Settings Panel (Grid Layout) ---
        settings_frame = ttk.LabelFrame(main_frame, text="Simulation Settings", padding="15")
        settings_frame.pack(fill=tk.X, pady=10)

        # 1. Protocol Selection
        ttk.Label(settings_frame, text="Protocol:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.protocol_var = tk.StringVar(value="AODV")
        self.protocol_combo = ttk.Combobox(
            settings_frame, 
            textvariable=self.protocol_var,
            values=["AODV", "DSR", "OLSR"],
            state="readonly",
            width=15
        )
        self.protocol_combo.grid(row=0, column=1, padx=5, pady=5)

        # 2. Node Count
        ttk.Label(settings_frame, text="Node Count:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.nodes_var = tk.StringVar(value="20")
        self.nodes_entry = ttk.Entry(settings_frame, textvariable=self.nodes_var, width=10)
        self.nodes_entry.grid(row=0, column=3, padx=5, pady=5)

        # 3. Simulation Time
        ttk.Label(settings_frame, text="Time (sec):").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.time_var = tk.StringVar(value="100")
        self.time_entry = ttk.Entry(settings_frame, textvariable=self.time_var, width=10)
        self.time_entry.grid(row=0, column=5, padx=5, pady=5)

        # --- AODV İnce Ayar Parametreleri (Row 1) ---
        ttk.Label(settings_frame, text="AODV Route Timeout (s):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.aodv_timeout_var = tk.StringVar(value="3.0")
        self.aodv_timeout_entry = ttk.Entry(settings_frame, textvariable=self.aodv_timeout_var, width=10)
        self.aodv_timeout_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="AODV Hello Interval (s):").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.aodv_hello_var = tk.StringVar(value="1.0")
        self.aodv_hello_entry = ttk.Entry(settings_frame, textvariable=self.aodv_hello_var, width=10)
        self.aodv_hello_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(settings_frame, text="AODV Hello Loss:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.aodv_hello_loss_var = tk.StringVar(value="2")
        self.aodv_hello_loss_entry = ttk.Entry(settings_frame, textvariable=self.aodv_hello_loss_var, width=10)
        self.aodv_hello_loss_entry.grid(row=1, column=5, padx=5, pady=5)

        # --- Simülasyon Kontrol Parametreleri (Row 2) ---
        ttk.Label(settings_frame, text="Random Seed:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.seed_var = tk.StringVar(value="0")
        self.seed_entry = ttk.Entry(settings_frame, textvariable=self.seed_var, width=10)
        self.seed_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Traffic Pairs:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.traffic_pairs_var = tk.StringVar(value="3")
        self.traffic_pairs_entry = ttk.Entry(settings_frame, textvariable=self.traffic_pairs_var, width=10)
        self.traffic_pairs_entry.grid(row=2, column=3, padx=5, pady=5)

        # Açıklama etiketi
        info_label = ttk.Label(settings_frame, text="(Aynı seed = aynı sonuç, farklı seed = farklı senaryo)", 
                              font=("Helvetica", 8, "italic"), foreground="gray")
        info_label.grid(row=2, column=4, columnspan=2, padx=5, pady=5, sticky="w")

        # --- Network Environment Parametreleri (Row 3) ---
        ttk.Label(settings_frame, text="Area Size (m):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.area_var = tk.StringVar(value="500")
        self.area_entry = ttk.Entry(settings_frame, textvariable=self.area_var, width=10)
        self.area_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Radio Range (m):").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.range_var = tk.StringVar(value="150")
        self.range_entry = ttk.Entry(settings_frame, textvariable=self.range_var, width=10)
        self.range_entry.grid(row=3, column=3, padx=5, pady=5)

        # Network ortamı açıklaması
        env_info_label = ttk.Label(settings_frame, text="(Küçük alan + kısa menzil = zor senaryo)", 
                              font=("Helvetica", 8, "italic"), foreground="gray")
        env_info_label.grid(row=3, column=4, columnspan=2, padx=5, pady=5, sticky="w")

        # --- Mobilite Parametreleri (Row 4) ---
        ttk.Label(settings_frame, text="Min Speed (m/s):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.min_speed_var = tk.StringVar(value="1.0")
        self.min_speed_entry = ttk.Entry(settings_frame, textvariable=self.min_speed_var, width=10)
        self.min_speed_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Max Speed (m/s):").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.max_speed_var = tk.StringVar(value="5.0")
        self.max_speed_entry = ttk.Entry(settings_frame, textvariable=self.max_speed_var, width=10)
        self.max_speed_entry.grid(row=4, column=3, padx=5, pady=5)

        ttk.Label(settings_frame, text="Pause Time (s):").grid(row=4, column=4, padx=5, pady=5, sticky="w")
        self.pause_var = tk.StringVar(value="2.0")
        self.pause_entry = ttk.Entry(settings_frame, textvariable=self.pause_var, width=10)
        self.pause_entry.grid(row=4, column=5, padx=5, pady=5)

        # --- Buttons ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)

        self.run_btn = ttk.Button(
            btn_frame, 
            text="Start Simulation", 
            command=self.start_simulation_thread
        )
        self.run_btn.pack(side=tk.LEFT, padx=10)

        ttk.Button(
            btn_frame, 
            text="Exit", 
            command=self.root.quit
        ).pack(side=tk.LEFT, padx=10)

        # --- Results Panel ---
        results_frame = ttk.LabelFrame(main_frame, text="Simulation Results & Logs", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(results_frame, height=15, font=("Consolas", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        self.log("System ready. Please select a protocol and click 'Start'.")

    def log(self, message):
        """Writes message to the text box in the GUI."""
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)

    def start_simulation_thread(self):
        """Runs simulation in a separate thread to prevent GUI freeze."""
        if not self.omnet_manager:
            messagebox.showerror("Error", "Cannot proceed: OMNeT++ Manager failed to initialize.")
            return

        # Disable button
        self.run_btn.config(state=tk.DISABLED)
        self.log("Starting process...")

        threading.Thread(target=self.run_omnet_simulation, daemon=True).start()

    def run_omnet_simulation(self):
        try:
            # Get parameters
            protocol = self.protocol_var.get()
            try:
                num_nodes = int(self.nodes_var.get())
                sim_time_val = int(self.time_var.get())
                sim_time = f"{sim_time_val}s"
                
                # AODV fine-tuning parameters
                aodv_timeout = float(self.aodv_timeout_var.get())
                aodv_hello = float(self.aodv_hello_var.get())
                aodv_hello_loss = int(self.aodv_hello_loss_var.get())
                
                # Simulation control parameters
                seed = int(self.seed_var.get())
                traffic_pairs = int(self.traffic_pairs_var.get())
                
                # Network environment parameters (YENİ)
                area_size = int(self.area_var.get())
                radio_range = int(self.range_var.get())
                min_speed = float(self.min_speed_var.get())
                max_speed = float(self.max_speed_var.get())
                pause_time = float(self.pause_var.get())
            except ValueError:
                self.log("ERROR: All parameters must be numeric.")
                return

            self.log(f"Preparing configuration: {protocol}, {num_nodes} Nodes, {sim_time}")
            self.log(f"Simulation Control: Seed={seed}, Traffic Pairs={traffic_pairs}")
            self.log(f"Network Environment: Area={area_size}m, Range={radio_range}m, Speed={min_speed}-{max_speed}m/s, Pause={pause_time}s")
            if protocol.upper() == "AODV":
                self.log(f"AODV Parameters: Route Timeout={aodv_timeout}s, Hello Interval={aodv_hello}s, Hello Loss={aodv_hello_loss}")

            # 1. Create Config
            self.omnet_manager.create_config(
                protocol=protocol, 
                num_nodes=num_nodes, 
                sim_time_limit=sim_time,
                aodv_timeout=aodv_timeout,
                aodv_hello_interval=aodv_hello,
                aodv_hello_loss=aodv_hello_loss,
                seed=seed,
                num_traffic_pairs=traffic_pairs,
                # Network environment parameters (YENİ)
                area_size=f"{area_size}m",
                radio_range=radio_range,
                min_speed=min_speed,
                max_speed=max_speed,
                pause_time=pause_time
            )
            
            # 2. Run Simulation
            self.log("Running OMNeT++ Simulation... (This may take a while)")
            success = self.omnet_manager.run_simulation()

            if success:
                self.log("Simulation completed successfully. Reading results...")
                # 3. Parse Results
                stats = self.omnet_manager.parse_results()
                
                # Display Results
                result_msg = (
                    f"\n{'='*40}\n"
                    f"RESULTS REPORT ({protocol})\n"
                    f"{'='*40}\n"
                    f"Packets Sent     : {stats.get('sent', 0)}\n"
                    f"Packets Received : {stats.get('received', 0)}\n"
                    f"------------------------\n"
                    f"PDR (Success)    : {stats.get('pdr', 0.0):.2f}%\n"
                    f"{'='*40}\n"
                )
                self.log(result_msg)
                
                if stats.get('sent', 0) == 0:
                    self.log("WARNING: No packets were sent.")
                elif stats.get('received', 0) == 0:
                    self.log("WARNING: No packets received. Try increasing simulation time or changing node count.")
            else:
                self.log("ERROR: Simulation failed. Check terminal output for error messages.")

        except Exception as e:
            self.log(f"CRITICAL ERROR: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
        finally:
            # Re-enable button (using after to run in main thread)
            self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))
