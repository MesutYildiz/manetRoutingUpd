"""
MANET Simulator GUI - OMNeT++ / INETMANET-3.x Controller

With Monte Carlo support and Graph visualization.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging

# Import our manager module
from omnet_manager import OmnetManager

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MANETSimulatorGUI:
    """
    OMNeT++ Control Panel with Monte Carlo and Graph support.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("MANET Simulator - OMNeT++ Controller")
        
        # Window size and position
        window_width = 900
        window_height = 700
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

        # Storage for Monte Carlo results (for graphing)
        self.monte_carlo_results = {}  # {protocol: [pdr1, pdr2, ...]}
        
        # Create GUI widgets
        self.create_widgets()

    def create_widgets(self):
        # --- Main Frame ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Title ---
        title_label = ttk.Label(
            main_frame, 
            text="OMNeT++ / INETMANET Simulation Control", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 15))

        # --- Settings Panel (Grid Layout) ---
        settings_frame = ttk.LabelFrame(main_frame, text="Simulation Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=5)

        # 1. Protocol Selection
        ttk.Label(settings_frame, text="Protocol:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.protocol_var = tk.StringVar(value="AODV")
        self.protocol_combo = ttk.Combobox(
            settings_frame, 
            textvariable=self.protocol_var,
            values=["AODV", "DSDV", "DSR", "OLSR", "DYMO", "BATMAN"],
            state="readonly",
            width=12
        )
        self.protocol_combo.grid(row=0, column=1, padx=5, pady=5)

        # 2. Node Count
        ttk.Label(settings_frame, text="Nodes:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.nodes_var = tk.StringVar(value="20")
        self.nodes_entry = ttk.Entry(settings_frame, textvariable=self.nodes_var, width=8)
        self.nodes_entry.grid(row=0, column=3, padx=5, pady=5)

        # 3. Simulation Time
        ttk.Label(settings_frame, text="Time (s):").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.time_var = tk.StringVar(value="100")
        self.time_entry = ttk.Entry(settings_frame, textvariable=self.time_var, width=8)
        self.time_entry.grid(row=0, column=5, padx=5, pady=5)

        # --- Row 1: Monte Carlo and Traffic ---
        ttk.Label(settings_frame, text="Start Seed:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.seed_var = tk.StringVar(value="0")
        self.seed_entry = ttk.Entry(settings_frame, textvariable=self.seed_var, width=8)
        self.seed_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Monte Carlo Runs:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.monte_carlo_var = tk.StringVar(value="5")
        self.monte_carlo_entry = ttk.Entry(settings_frame, textvariable=self.monte_carlo_var, width=8)
        self.monte_carlo_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(settings_frame, text="Traffic Pairs:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.traffic_pairs_var = tk.StringVar(value="3")
        self.traffic_pairs_entry = ttk.Entry(settings_frame, textvariable=self.traffic_pairs_var, width=8)
        self.traffic_pairs_entry.grid(row=1, column=5, padx=5, pady=5)

        # --- Row 2: Network Environment ---
        ttk.Label(settings_frame, text="Area (m):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.area_var = tk.StringVar(value="500")
        self.area_entry = ttk.Entry(settings_frame, textvariable=self.area_var, width=8)
        self.area_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Range (m):").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.range_var = tk.StringVar(value="150")
        self.range_entry = ttk.Entry(settings_frame, textvariable=self.range_var, width=8)
        self.range_entry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(settings_frame, text="Speed (m/s):").grid(row=2, column=4, padx=5, pady=5, sticky="w")
        speed_frame = ttk.Frame(settings_frame)
        speed_frame.grid(row=2, column=5, padx=5, pady=5)
        self.min_speed_var = tk.StringVar(value="1.0")
        self.max_speed_var = tk.StringVar(value="5.0")
        ttk.Entry(speed_frame, textvariable=self.min_speed_var, width=4).pack(side=tk.LEFT)
        ttk.Label(speed_frame, text="-").pack(side=tk.LEFT)
        ttk.Entry(speed_frame, textvariable=self.max_speed_var, width=4).pack(side=tk.LEFT)

        # --- Row 3: AODV Parameters ---
        ttk.Label(settings_frame, text="AODV Timeout:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.aodv_timeout_var = tk.StringVar(value="3.0")
        self.aodv_timeout_entry = ttk.Entry(settings_frame, textvariable=self.aodv_timeout_var, width=8)
        self.aodv_timeout_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Hello Interval:").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.aodv_hello_var = tk.StringVar(value="1.0")
        self.aodv_hello_entry = ttk.Entry(settings_frame, textvariable=self.aodv_hello_var, width=8)
        self.aodv_hello_entry.grid(row=3, column=3, padx=5, pady=5)

        ttk.Label(settings_frame, text="Hello Loss:").grid(row=3, column=4, padx=5, pady=5, sticky="w")
        self.aodv_hello_loss_var = tk.StringVar(value="2")
        self.aodv_hello_loss_entry = ttk.Entry(settings_frame, textvariable=self.aodv_hello_loss_var, width=8)
        self.aodv_hello_loss_entry.grid(row=3, column=5, padx=5, pady=5)

        # Pause time (hidden but needed)
        self.pause_var = tk.StringVar(value="2.0")

        # --- Buttons Frame ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)

        # Run Single Protocol
        self.run_btn = ttk.Button(
            btn_frame, 
            text="▶ Run Selected Protocol", 
            command=self.start_simulation_thread
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)

        # Compare All Protocols
        self.compare_btn = ttk.Button(
            btn_frame, 
            text="📊 Compare All Protocols", 
            command=self.start_comparison_thread
        )
        self.compare_btn.pack(side=tk.LEFT, padx=5)

        # Show Graph
        self.graph_btn = ttk.Button(
            btn_frame, 
            text="📈 Show Graph", 
            command=self.show_graph,
            state=tk.DISABLED
        )
        self.graph_btn.pack(side=tk.LEFT, padx=5)

        # Clear Results
        ttk.Button(
            btn_frame, 
            text="🗑 Clear", 
            command=self.clear_results
        ).pack(side=tk.LEFT, padx=5)

        # Exit
        ttk.Button(
            btn_frame, 
            text="Exit", 
            command=self.root.quit
        ).pack(side=tk.LEFT, padx=5)

        # --- Results Panel ---
        results_frame = ttk.LabelFrame(main_frame, text="Simulation Results & Logs", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(results_frame, height=18, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        self.log("System ready.")
        self.log("• 'Run Selected Protocol' - Monte Carlo simulation for one protocol")
        self.log("• 'Compare All Protocols' - Run all protocols with same settings")
        self.log("• 'Show Graph' - Display comparison chart (after running simulations)")

    def log(self, message):
        """Writes message to the text box in the GUI."""
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)

    def clear_results(self):
        """Clear all stored results and log."""
        self.monte_carlo_results = {}
        self.log_text.delete(1.0, tk.END)
        self.log("Results cleared.")
        self.graph_btn.config(state=tk.DISABLED)

    def get_params(self):
        """Get all parameters from GUI."""
        try:
            params = {
                'protocol': self.protocol_var.get(),
                'num_nodes': int(self.nodes_var.get()),
                'sim_time': f"{int(self.time_var.get())}s",
                'start_seed': int(self.seed_var.get()),
                'monte_carlo_runs': int(self.monte_carlo_var.get()),
                'traffic_pairs': int(self.traffic_pairs_var.get()),
                'area_size': int(self.area_var.get()),
                'radio_range': int(self.range_var.get()),
                'min_speed': float(self.min_speed_var.get()),
                'max_speed': float(self.max_speed_var.get()),
                'pause_time': float(self.pause_var.get()),
                'aodv_timeout': float(self.aodv_timeout_var.get()),
                'aodv_hello': float(self.aodv_hello_var.get()),
                'aodv_hello_loss': int(self.aodv_hello_loss_var.get()),
            }
            return params
        except ValueError as e:
            self.log(f"ERROR: Invalid parameter value - {e}")
            return None

    def start_simulation_thread(self):
        """Run single protocol simulation in thread."""
        if not self.omnet_manager:
            messagebox.showerror("Error", "OMNeT++ Manager not initialized.")
            return
        
        self.run_btn.config(state=tk.DISABLED)
        self.compare_btn.config(state=tk.DISABLED)
        self.log("Starting simulation...")
        threading.Thread(target=self.run_single_protocol, daemon=True).start()

    def start_comparison_thread(self):
        """Run all protocols comparison in thread."""
        if not self.omnet_manager:
            messagebox.showerror("Error", "OMNeT++ Manager not initialized.")
            return
        
        self.run_btn.config(state=tk.DISABLED)
        self.compare_btn.config(state=tk.DISABLED)
        self.log("Starting protocol comparison...")
        threading.Thread(target=self.run_all_protocols, daemon=True).start()

    def run_single_protocol(self):
        """Run Monte Carlo simulation for selected protocol."""
        try:
            params = self.get_params()
            if not params:
                return

            protocol = params['protocol']
            monte_carlo_runs = params['monte_carlo_runs']
            
            self.log(f"\n{'='*50}")
            self.log(f"Protocol: {protocol}")
            self.log(f"Monte Carlo Runs: {monte_carlo_runs}")
            self.log(f"{'='*50}")

            pdr_results = self._run_monte_carlo(protocol, params)
            
            if pdr_results:
                self.monte_carlo_results[protocol] = pdr_results
                self._display_statistics(protocol, pdr_results)
                self.graph_btn.config(state=tk.NORMAL)

        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
        finally:
            self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.compare_btn.config(state=tk.NORMAL))

    def run_all_protocols(self):
        """Run Monte Carlo for all protocols."""
        try:
            params = self.get_params()
            if not params:
                return

            # Protocols to compare (excluding DSDV which has issues)
            protocols = ["AODV", "DSR", "OLSR", "DYMO", "BATMAN"]
            
            self.log(f"\n{'='*60}")
            self.log(f"🔬 PROTOCOL COMPARISON - Monte Carlo x{params['monte_carlo_runs']}")
            self.log(f"Settings: {params['num_nodes']} Nodes, {params['area_size']}m Area, {params['radio_range']}m Range")
            self.log(f"{'='*60}")

            # Clear previous results
            self.monte_carlo_results = {}

            for protocol in protocols:
                self.log(f"\n--- Running {protocol} ---")
                pdr_results = self._run_monte_carlo(protocol, params)
                
                if pdr_results:
                    self.monte_carlo_results[protocol] = pdr_results
                    self._display_statistics(protocol, pdr_results, compact=True)

            # Final Summary
            self._display_final_summary()
            self.graph_btn.config(state=tk.NORMAL)

        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
        finally:
            self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.compare_btn.config(state=tk.NORMAL))

    def _run_monte_carlo(self, protocol, params):
        """Run Monte Carlo simulation and return PDR results."""
        pdr_results = []
        
        for run_idx in range(params['monte_carlo_runs']):
            current_seed = params['start_seed'] + run_idx
            
            # Create config
            self.omnet_manager.create_config(
                protocol=protocol,
                num_nodes=params['num_nodes'],
                sim_time_limit=params['sim_time'],
                aodv_timeout=params['aodv_timeout'],
                aodv_hello_interval=params['aodv_hello'],
                aodv_hello_loss=params['aodv_hello_loss'],
                seed=current_seed,
                num_traffic_pairs=params['traffic_pairs'],
                area_size=f"{params['area_size']}m",
                radio_range=params['radio_range'],
                min_speed=params['min_speed'],
                max_speed=params['max_speed'],
                pause_time=params['pause_time']
            )
            
            # Run simulation
            success = self.omnet_manager.run_simulation()
            
            if success:
                stats = self.omnet_manager.parse_results()
                pdr = stats.get('pdr', 0.0)
                pdr_results.append(pdr)
                self.log(f"  Seed {current_seed}: PDR = {pdr:.2f}%")
            else:
                self.log(f"  Seed {current_seed}: FAILED")
                pdr_results.append(0.0)
        
        return pdr_results

    def _display_statistics(self, protocol, pdr_results, compact=False):
        """Display statistics for a protocol's results."""
        import statistics
        
        valid_results = [p for p in pdr_results if p > 0]
        
        if not valid_results:
            self.log(f"  No valid results for {protocol}")
            return
        
        avg = statistics.mean(valid_results)
        std = statistics.stdev(valid_results) if len(valid_results) > 1 else 0
        min_val = min(valid_results)
        max_val = max(valid_results)
        
        if compact:
            self.log(f"  → {protocol}: Avg={avg:.1f}% ±{std:.1f}% (Min={min_val:.1f}%, Max={max_val:.1f}%)")
        else:
            self.log(f"\n📊 {protocol} Statistics:")
            self.log(f"   Average PDR : {avg:.2f}%")
            self.log(f"   Std Dev     : {std:.2f}%")
            self.log(f"   Min         : {min_val:.2f}%")
            self.log(f"   Max         : {max_val:.2f}%")
            self.log(f"   All values  : {[f'{p:.1f}%' for p in pdr_results]}")

    def _display_final_summary(self):
        """Display final comparison summary."""
        import statistics
        
        self.log(f"\n{'='*60}")
        self.log("📊 FINAL COMPARISON SUMMARY")
        self.log(f"{'='*60}")
        
        # Calculate stats and sort by average PDR
        summary = []
        for protocol, results in self.monte_carlo_results.items():
            valid = [p for p in results if p > 0]
            if valid:
                avg = statistics.mean(valid)
                std = statistics.stdev(valid) if len(valid) > 1 else 0
                summary.append((protocol, avg, std))
        
        # Sort by average PDR (descending)
        summary.sort(key=lambda x: x[1], reverse=True)
        
        # Display ranking
        medals = ["🥇", "🥈", "🥉", "4.", "5.", "6."]
        self.log(f"\n{'Rank':<6}{'Protocol':<10}{'Avg PDR':<12}{'Std Dev':<10}")
        self.log("-" * 40)
        
        for i, (protocol, avg, std) in enumerate(summary):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            self.log(f"{medal:<6}{protocol:<10}{avg:>6.2f}%{std:>10.2f}%")
        
        self.log(f"\n{'='*60}")
        self.log("💡 Click 'Show Graph' to visualize the results!")

    def show_graph(self):
        """Display comparison graph using matplotlib."""
        if not self.monte_carlo_results:
            messagebox.showwarning("No Data", "No simulation results to display. Run a simulation first.")
            return
        
        try:
            import matplotlib.pyplot as plt
            import statistics
            import numpy as np
        except ImportError:
            messagebox.showerror("Error", "matplotlib is required.\nInstall with: pip install matplotlib")
            return
        
        # Prepare data
        protocols = []
        averages = []
        std_devs = []
        all_values = []
        
        for protocol, results in self.monte_carlo_results.items():
            valid = [p for p in results if p > 0]
            if valid:
                protocols.append(protocol)
                averages.append(statistics.mean(valid))
                std_devs.append(statistics.stdev(valid) if len(valid) > 1 else 0)
                all_values.append(valid)
        
        if not protocols:
            messagebox.showwarning("No Data", "No valid results to display.")
            return
        
        # Sort by average (descending)
        sorted_data = sorted(zip(protocols, averages, std_devs, all_values), 
                           key=lambda x: x[1], reverse=True)
        protocols, averages, std_devs, all_values = zip(*sorted_data)
        
        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('MANET Protocol Performance Comparison (Monte Carlo)', fontsize=14, fontweight='bold')
        
        # Colors for protocols
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
        
        # --- Graph 1: Bar Chart with Error Bars ---
        x = np.arange(len(protocols))
        bars = ax1.bar(x, averages, yerr=std_devs, capsize=5, color=colors[:len(protocols)], 
                       edgecolor='black', linewidth=1.2, alpha=0.8)
        
        ax1.set_xlabel('Protocol', fontsize=12)
        ax1.set_ylabel('Average PDR (%)', fontsize=12)
        ax1.set_title('Average PDR with Standard Deviation', fontsize=12)
        ax1.set_xticks(x)
        ax1.set_xticklabels(protocols, fontsize=11)
        ax1.set_ylim(0, 100)
        ax1.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='50% threshold')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar, avg, std in zip(bars, averages, std_devs):
            height = bar.get_height()
            ax1.annotate(f'{avg:.1f}%\n±{std:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
        
        # --- Graph 2: Box Plot ---
        bp = ax2.boxplot(all_values, labels=protocols, patch_artist=True)
        
        for patch, color in zip(bp['boxes'], colors[:len(protocols)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax2.set_xlabel('Protocol', fontsize=12)
        ax2.set_ylabel('PDR (%)', fontsize=12)
        ax2.set_title('PDR Distribution (Box Plot)', fontsize=12)
        ax2.set_ylim(0, 100)
        ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        self.log("\n📈 Graph displayed in separate window.")


def main():
    root = tk.Tk()
    app = MANETSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
