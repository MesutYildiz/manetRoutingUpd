"""
OMNeT++ Manager - Python controller for OMNeT++ and INETMANET simulation engine

Kesin Çözüm: Protokol ve Host Tipi Standardizasyonu
- Her protokol için özel host tipi kullanılıyor (uyumsuzluk çözümü)
- AODV için AODVRouter, DSR için DYMORouter, OLSR için AdhocHost
- libINET.dll PATH sorunu çözüldü
"""

import os
import subprocess
import re
from pathlib import Path
from typing import Dict, Optional, List
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OmnetManager:
    """
    OMNeT++ Simülasyonlarını yöneten sınıf.
    
    Kesin Çözüm: Her protokol için özel host tipi kullanılıyor
    """

    def __init__(self, omnet_executable: str = None, working_directory: str = None, 
                 library_path: str = None, ned_path: str = None):
        """
        OMNeT++ Manager'ı başlat.
        """
        # SABİT YOLLAR (Kullanıcının bilgisayarına özel)
        self.omnet_executable = omnet_executable or r"C:\omnetpp-5.6.2\bin\opp_run.exe"
        self.working_dir = working_directory or r"C:\Users\W11\OneDrive\Desktop\Manet_Projem\inetmanet-3.0"
        self.library_path = library_path or "INET"
        self.ned_path = ned_path or "src;examples"
        
        # Sonuçların kaydedileceği yer
        self.results_dir = os.path.join(self.working_dir, "results")
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Config dosyası yolu
        self.config_file = os.path.join(self.working_dir, "omnetpp.ini")
        
        logger.info(f"OMNeT++ Manager initialized: {self.omnet_executable}")

    def ensure_config_exists(self):
        """Config dosyası kontrolü - create_config ile sıfırdan yapılıyor"""
        pass

    def create_config(self, protocol="AODV", num_nodes=10, sim_time_limit="100s", 
                     network_name=None, mobility_model="RandomWPMobility",
                     min_speed=1.0, max_speed=5.0, pause_time=2.0, area_size="500m",
                     radio_power=20.0, radio_range=250.0, bitrate="2Mbps",
                     aodv_timeout=3.0, aodv_hello_interval=1.0, aodv_hello_loss=2,
                     seed=0, num_traffic_pairs=3):
        """
        OMNeT++ için .ini dosyasını sıfırdan, garantili ayarlarla oluşturur.
        Kesin Çözüm: Her protokol için özel host tipi kullanılıyor (Altın Anahtar Stratejisi)
        """
        # 1. PROTOKOL VE NETWORK STRATEJİSİ (Her Protokol İçin En Uygun Yapı)
        # AODV: Özel router kullan (daha önce çalışıyordu)
        # DSR: DYMO Router kullan - radyo ayarlarını override etme (kendi ayarlarını kullan)
        # OLSR: AdhocHost ile deneyelim (eğer çalışmazsa alternatif)
        protocol_upper = protocol.upper()
        use_custom_radio = True  # Varsayılan: radyo ayarlarını override et
        
        if protocol_upper == "AODV":
            # AODV için çalışan yapıyı geri getiriyoruz
            if network_name is None or network_name.strip() == "":
                network_name = "inet.examples.aodv.AODVNetwork"
            host_type = "inet.node.aodv.AODVRouter"
            routing_conf = ""  # Router içinde gömülü
            use_custom_radio = True  # AODV için IdealWirelessNic kullan
            
        elif protocol_upper == "DSR":
            # DSR için DYMO router kullan - radyo ayarlarını override ETME
            if network_name is None or network_name.strip() == "":
                network_name = "inet.examples.manetrouting.dymo.DYMONetwork"
            host_type = "inet.node.dymo.DYMORouter"
            routing_conf = '*.host[*].routingProtocol = "inet.routing.dymo.DYMO"'
            use_custom_radio = False  # DYMONetwork kendi radyo ayarlarını kullanacak
            
        elif protocol_upper == "OLSR":
            # OLSR için AdhocHost deneyelim (çalışmazsa başka çözüm)
            if network_name is None or network_name.strip() == "":
                network_name = "inet.examples.adhoc.ieee80211.Net80211"
            host_type = "inet.node.inet.AdhocHost"
            routing_conf = '*.host[*].routingProtocol = "inet.routing.extras.olsr.OLSR"'
            use_custom_radio = True
            
        else:
            # Varsayılan: AODV yapısı
            if network_name is None or network_name.strip() == "":
                network_name = "inet.examples.aodv.AODVNetwork"
            host_type = "inet.node.aodv.AODVRouter"
            routing_conf = ""
            use_custom_radio = True
        
        if network_name and network_name.strip():
            network_name = network_name.strip()
        else:
            network_name = "inet.examples.adhoc.ieee80211.Net80211"

        # 2. RADYO AYARLARI (Protokole Özel)
        if use_custom_radio:
            # AODV ve diğerleri için IdealWirelessNic
            # Menzil artık GUI'den gelen radio_range parametresinden alınıyor
            radio_config = f"""# Radyo Ayarları - IdealWirelessNic
# Menzil: {radio_range}m (GUI'den ayarlanabilir)
*.host[*].wlan[*].typename = "IdealWirelessNic"
*.host[*].wlan[*].bitrate = {bitrate}
*.host[*].wlan[*].mac.useAck = false
*.host[*].wlan[*].mac.fullDuplex = false
*.host[*].wlan[*].radio.transmitter.typename = "IdealTransmitter"
*.host[*].wlan[*].radio.transmitter.communicationRange = {radio_range}m
*.host[*].wlan[*].radio.transmitter.power = 1mW
*.host[*].wlan[*].radio.transmitter.headerBitLength = 100b"""
        else:
            # DSR için: DYMONetwork kendi radyo ayarlarını kullanacak (override etme)
            radio_config = "# Radyo Ayarları: DYMONetwork kendi varsayılan radyo ayarlarını kullanıyor (override edilmedi)"

        # 3. AODV İNCE AYARLARI (Protokole Özel)
        aodv_settings = ""
        if protocol_upper == "AODV":
            aodv_settings = f"""
# --- AODV İNCE AYARLAR (Fine-Tuning Parameters) ---
# Rota Geçerlilik Süresi: Bir rota kullanılmadığında ne kadar süre sonra silinir
*.host[*].aodv.activeRouteTimeout = {aodv_timeout}s

# Hello Mesajı Sıklığı: Node'ların komşularına "Ben buradayım" deme sıklığı
*.host[*].aodv.helloInterval = {aodv_hello_interval}s

# İzin Verilen Hello Kaybı: Kaç Hello mesajı gelmezse komşunun öldüğü varsayılır
*.host[*].aodv.allowedHelloLoss = {aodv_hello_loss}

# Diğer AODV Ayarları (Varsayılan değerler)
*.host[*].aodv.netDiameter = 35
*.host[*].aodv.rreqRetries = 2
*.host[*].aodv.rreqRatelimit = 10
"""

        # 4. KONFİGÜRASYON İÇERİĞİ
        
        # Dinamik trafik çiftleri oluştur (daha fazla kaynak-hedef çifti = daha stabil sonuçlar)
        traffic_config = self._generate_traffic_config(num_nodes, num_traffic_pairs)
        
        config_content = f"""[General]
network = {network_name}
sim-time-limit = {sim_time_limit}
cpu-time-limit = 300s
record-eventlog = false
cmdenv-express-mode = true

# --- DETERMINISTIK SIMÜLASYON İÇİN KRİTİK ---
# Aynı seed = aynı sonuçlar (tekrarlanabilirlik)
seed-set = {seed}
repeat = 1

# RNG (Random Number Generator) Seed Kontrolü
# Tüm modüller için aynı seed'i kullan
**.rng-0 = {seed}
num-rngs = 1

# --- NETWORK VE HOST AYARLARI ---
*.numHosts = {num_nodes}
*.host[*].typename = "{host_type}"

# --- PROTOKOL AYARLARI ---
{routing_conf}
{aodv_settings}

# --- MOBILITE (ALTIN VURUŞ: SINIR ALANLARI EKLENDİ) ---
# RandomWPMobility bu sınırlar olmadan çalışmaz!
# "Cannot schedule message ... move to the past" hatasını önlemek için kritik:
*.host[*].mobilityType = "RandomWPMobility"
*.host[*].mobility.initFromDisplayString = false
*.host[*].mobility.updateInterval = 0.1s
*.host[*].mobility.startTime = 0s

# Hız ve Bekleme
*.host[*].mobility.speed = uniform({min_speed}mps, {max_speed}mps)
*.host[*].mobility.waitTime = uniform({pause_time}s, {pause_time}s)

# Başlangıç Pozisyonları
*.host[*].mobility.x = uniform(0m, {area_size})
*.host[*].mobility.y = uniform(0m, {area_size})
*.host[*].mobility.z = 0m

# HAREKET SINIRLARI (BU EKSİKTİ - KRİTİK!)
# RandomWPMobility bu sınırlar olmadan rastgele hedef seçemez ve çöker
*.host[*].mobility.constraintAreaMinX = 0m
*.host[*].mobility.constraintAreaMinY = 0m
*.host[*].mobility.constraintAreaMinZ = 0m
*.host[*].mobility.constraintAreaMaxX = {area_size}
*.host[*].mobility.constraintAreaMaxY = {area_size}
*.host[*].mobility.constraintAreaMaxZ = 0m

# Playground Boyutu
**.playgroundSizeX = {area_size}
**.playgroundSizeY = {area_size}

# --- TRAFİK (UDP - Çoklu Kaynak-Hedef Çiftleri) ---
# Birden fazla trafik çifti = daha stabil ve güvenilir sonuçlar
{traffic_config}

# --- RADYO VE IP AYARLARI ---
# Dosya arama hatasını önlemek için inline XML
*.configurator.config = xml("<config><interface hosts='**' address='10.0.0.x' netmask='255.255.255.0'/></config>")
*.configurator.addStaticRoutes = false
*.configurator.assignAddresses = true

# Radyo Ayarları - Protokole Özel
{radio_config}

# İstatistik kayıt ayarları (sonuç parse için gerekli)
**.scalar-recording = true
**.vector-recording = false
**.cmdenv-log-level = info
"""

        # Dosyayı UTF-8 olarak kaydet
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                f.write(config_content)
            
            logger.info(f"[PYTHON] Konfigürasyon oluşturuldu: {protocol} -> {host_type} (Network: {network_name})")
            return self.config_file
            
        except Exception as e:
            logger.error(f"Config oluşturma hatası: {e}")
            raise

    def _generate_traffic_config(self, num_nodes: int, num_pairs: int) -> str:
        """
        Çoklu kaynak-hedef çiftleri için trafik konfigürasyonu oluşturur.
        
        Avantajları:
        - Tek bir bağlantının kopması tüm sonucu etkilemez
        - Daha gerçekçi MANET trafiği
        - Daha stabil PDR değerleri
        
        Args:
            num_nodes: Toplam node sayısı
            num_pairs: Kaç tane kaynak-hedef çifti oluşturulacak
        
        Returns:
            OMNeT++ config formatında trafik ayarları string'i
        """
        # En az 4 node gerekli (2 çift için)
        if num_nodes < 4:
            num_pairs = 1
        
        # Maksimum çift sayısı = num_nodes / 2
        max_pairs = num_nodes // 2
        num_pairs = min(num_pairs, max_pairs)
        
        config_lines = []
        config_lines.append(f"# {num_pairs} adet kaynak-hedef çifti oluşturuluyor")
        config_lines.append(f"# Toplam node: {num_nodes}, Aktif trafik çifti: {num_pairs}")
        config_lines.append("")
        
        base_port = 5000
        
        for i in range(num_pairs):
            src_idx = i * 2        # 0, 2, 4, ...
            dst_idx = i * 2 + 1    # 1, 3, 5, ...
            port = base_port + i
            
            # Gönderen node ayarları
            config_lines.append(f"# --- Trafik Çifti {i+1}: host[{src_idx}] -> host[{dst_idx}] ---")
            config_lines.append(f"*.host[{src_idx}].numUdpApps = 1")
            config_lines.append(f'*.host[{src_idx}].udpApp[0].typename = "UDPBasicApp"')
            config_lines.append(f'*.host[{src_idx}].udpApp[0].destAddresses = "host[{dst_idx}]"')
            config_lines.append(f"*.host[{src_idx}].udpApp[0].destPort = {port}")
            config_lines.append(f"*.host[{src_idx}].udpApp[0].messageLength = 512B")
            config_lines.append(f"*.host[{src_idx}].udpApp[0].sendInterval = 0.5s")
            config_lines.append(f"*.host[{src_idx}].udpApp[0].startTime = {2 + i * 0.1}s")
            config_lines.append("")
            
            # Alıcı node ayarları
            config_lines.append(f"*.host[{dst_idx}].numUdpApps = 1")
            config_lines.append(f'*.host[{dst_idx}].udpApp[0].typename = "UDPSink"')
            config_lines.append(f"*.host[{dst_idx}].udpApp[0].localPort = {port}")
            config_lines.append("")
        
        return "\n".join(config_lines)

    def run_simulation(self):
        """
        Simülasyonu çalıştırır. DLL hatalarını önlemek için PATH ayarı yapar.
        """
        # DLL Yolları (libINET.dll için src klasörü EKLENDİ)
        omnet_root = r"C:\omnetpp-5.6.2"
        
        # libINET.dll için projenin src klasörünü PATH'e ekle (EN ÖNEMLİ!)
        src_dir = os.path.join(self.working_dir, "src")
        out_src_dir = os.path.join(self.working_dir, "out", "clang-release", "src")  # Derlenmiş DLL'ler burada olabilir
        
        paths_to_add = [
            src_dir,  # libINET.dll için src klasörü (EN BAŞA EKLENDİ)
            out_src_dir,  # Derlenmiş DLL'ler için out klasörü
            os.path.join(omnet_root, "bin"),
            os.path.join(omnet_root, "lib"),
            os.path.join(omnet_root, "tools", "win64", "mingw64", "bin")  # Kritik!
        ]
        
        # Yalnızca var olan klasörleri ekle
        existing_paths = [p for p in paths_to_add if os.path.exists(p)]
        
        # Yeni PATH oluştur
        env = os.environ.copy()
        env["OMNETPP_ROOT"] = omnet_root
        env["PATH"] = ";".join(existing_paths) + ";" + env.get("PATH", "")
        
        logger.info(f"DLL PATH'e eklendi: {existing_paths}")

        # Komut - Library path'i tam yol olarak belirt
        library_path_full = os.path.join(self.working_dir, "src", "INET")
        cmd = [
            self.omnet_executable,
            "-u", "Cmdenv",
            "-l", library_path_full,
            "-n", self.ned_path,
            "-f", "omnetpp.ini",
            "-c", "General",
            "-r", "0"  # KRİTİK: Run numarasını sabitleyerek seed'in çalışmasını garanti et
        ]

        logger.info(f"[PYTHON] Simülasyon Başlıyor... (Komut: {' '.join(cmd)})")
        logger.info(f"Working directory: {self.working_dir}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                env=env,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=600  # 10 dakika timeout
            )
            
            # STDOUT ve STDERR'i konsola yazdır
            if result.stdout:
                logger.info(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                logger.error(f"STDERR:\n{result.stderr}")
            
            if result.returncode != 0:
                logger.error(f"[PYTHON] SİMÜLASYON HATASI! Return code: {result.returncode}")
                if result.returncode == 3221225781:
                    logger.error("HATA: Access Violation (0xC0000005) - DLL eksik veya path yanlış!")
                    logger.error("Kontrol edin: MinGW bin klasörü PATH'e eklendi mi?")
                return False
                
            logger.info("[PYTHON] Simülasyon Başarıyla Tamamlandı.")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("[PYTHON] Simülasyon zaman aşımına uğradı (10 dakika)")
            return False
        except Exception as e:
            logger.error(f"[PYTHON] Beklenmeyen Hata: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def parse_results(self):
        """
        AKILLI PARSER - Sadece host[0] (gönderici) ve host[1] (alıcı) istatistiklerini okur.
        
        ÖNEMLİ: PDR'nin %100'ü aşması sorununun çözümü!
        Eski parser tüm ağ trafiğini (routing, hello, ack paketleri) sayıyordu.
        Bu parser sadece uygulama katmanı (UDP/Ping) trafiğini filtreler.
        """
        # En yeni .sca dosyasını bul
        sca_files = list(Path(self.results_dir).glob("*.sca"))
        
        if not sca_files:
            logger.warning("[PYTHON] Sonuç dosyası bulunamadı.")
            return {
                'sent': 0,
                'received': 0,
                'pdr': 0.0,
                'avg_delay': 0.0,
                'avg_hops': 0.0,
                'avg_throughput': 0.0
            }
        
        # En yeni dosyayı al
        latest_sca = max(sca_files, key=os.path.getmtime)
        
        stats = {
            'sent': 0,
            'received': 0,
            'pdr': 0.0,
            'avg_delay': 0.0,
            'avg_hops': 0.0,
            'avg_throughput': 0.0
        }
        
        try:
            with open(latest_sca, 'r', encoding="utf-8", errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    
                    # Sadece scalar satırlarına bak
                    if not line.startswith("scalar"):
                        continue
                    
                    parts = line.split()
                    if len(parts) < 4:
                        continue
                    
                    # Format: scalar <module_path> <stat_name> <value>
                    module_path = parts[1] if len(parts) > 1 else ""
                    stat_name = parts[2] if len(parts) > 2 else ""
                    value = parts[3] if len(parts) > 3 else "0"
                    
                    # ÇOKLU TRAFİK ÇİFTLERİ DESTEĞİ
                    # Tüm host'ların udpApp istatistiklerini topla
                    # Eski: sadece host[0] ve host[1]
                    # Yeni: tüm host'lar (host[0], host[2], host[4]... gönderir; host[1], host[3], host[5]... alır)
                    
                    if "udpApp" in module_path:
                        # Gönderilen paketler (çift indeksli host'lar: 0, 2, 4, ...)
                        if "sentPk:count" in stat_name or "packetSent:count" in stat_name:
                            try:
                                stats['sent'] += int(value)
                            except (ValueError, IndexError):
                                pass
                        
                        # Alınan paketler (tek indeksli host'lar: 1, 3, 5, ...)
                        if "rcvdPk:count" in stat_name or "packetReceived:count" in stat_name:
                            try:
                                stats['received'] += int(value)
                            except (ValueError, IndexError):
                                pass
                        
                        # DELAY - Alınan paketlerin gecikmesi
                        if "endToEndDelay:mean" in stat_name or "delay:mean" in stat_name or "pingRtt:mean" in stat_name:
                            try:
                                delay_val = float(value)
                                if stats['avg_delay'] == 0.0:
                                    stats['avg_delay'] = delay_val * 1000  # Saniyeden ms'ye
                            except (ValueError, IndexError):
                                pass
                    
                    # 4. HOPS - Ortalama hop sayısı (genel metrik)
                    if "hopCount:mean" in stat_name or "numHops:mean" in stat_name:
                        try:
                            hops_val = float(value)
                            if stats['avg_hops'] == 0.0:
                                stats['avg_hops'] = hops_val
                        except (ValueError, IndexError):
                            pass
                
                # PDR hesapla
                if stats['sent'] > 0:
                    stats['pdr'] = round((stats['received'] / stats['sent']) * 100.0, 2)
                    
                    # PDR %100'ü aşarsa uyarı ver
                    if stats['pdr'] > 100.0:
                        logger.warning(f"[UYARI] PDR %100'ü aşıyor ({stats['pdr']}%). Parsing kontrol edilmeli!")
                
                # Delay ve Hops'u yuvarla
                stats['avg_delay'] = round(stats['avg_delay'], 2)
                stats['avg_hops'] = round(stats['avg_hops'], 2)
                    
        except Exception as e:
            logger.error(f"[PYTHON] Sonuç okuma hatası: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
        logger.info(f"[PYTHON] Parse edilen sonuçlar: Sent={stats['sent']}, Received={stats['received']}, PDR={stats['pdr']}%")
        return stats

    def run_full_simulation(self, protocol="AODV", num_nodes=10, sim_time_limit="100s",
                           network_name=None, mobility_model="RandomWPMobility",
                           min_speed=1.0, max_speed=5.0, pause_time=2.0, area_size="500m",
                           radio_power=20.0, radio_range=250.0, bitrate="2Mbps"):
        """
        Tam simülasyon workflow'u: Config oluştur -> Çalıştır -> Parse et
        GUI uyumluluğu için gerekli metod
        """
        try:
            # 1. Config oluştur
            self.create_config(
                protocol=protocol,
                num_nodes=num_nodes,
                sim_time_limit=sim_time_limit,
                network_name=network_name,
                mobility_model=mobility_model,
                min_speed=min_speed,
                max_speed=max_speed,
                pause_time=pause_time,
                area_size=area_size,
                radio_power=radio_power,
                radio_range=radio_range,
                bitrate=bitrate
            )
            
            # 2. Simülasyonu çalıştır
            success = self.run_simulation()
            
            if not success:
                return {
                    'simulation_error': True,
                    'error_message': 'Simülasyon başarısız',
                    'sent': 0,
                    'received': 0,
                    'pdr': 0.0
                }
            
            # 3. Sonuçları parse et
            results = self.parse_results()
            results['simulation_error'] = False
            
            return results
            
        except Exception as e:
            logger.error(f"run_full_simulation hatası: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                'simulation_error': True,
                'error_message': str(e),
                'sent': 0,
                'received': 0,
                'pdr': 0.0
            }

    def find_available_networks(self) -> List[str]:
        """
        Examples klasöründeki .ned dosyalarını tarar ve tanımlı ağ isimlerini bulur.
        GUI'deki 'Scan Networks' butonu için.
        """
        networks = []
        examples_dir = os.path.join(self.working_dir, "examples")
        
        if not os.path.exists(examples_dir):
            logger.warning(f"Examples klasörü bulunamadı: {examples_dir}")
            return []
        
        logger.info("Ağlar taranıyor...")
        
        # Examples klasörünü özyineli (recursive) tara
        for root, dirs, files in os.walk(examples_dir):
            for file in files:
                if file.endswith(".ned"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # Regex ile "network X" tanımlarını bul
                        matches = re.findall(r'\bnetwork\s+(\w+)', content)
                        if matches:
                            for match in matches:
                                # Paket ismini (package x.y.z;) bulmaya çalış
                                pkg_match = re.search(r'\bpackage\s+([\w\.]+);', content)
                                if pkg_match:
                                    # Tam isim: package.NetworkName
                                    full_name = f"{pkg_match.group(1)}.{match}"
                                    networks.append(full_name)
                                networks.append(match)
                    except Exception as e:
                        logger.warning(f"Dosya okunamadı {file}: {e}")
        
        # Tekrarları temizle ve sırala
        networks = sorted(list(set(networks)))
        logger.info(f"Bulunan ağlar: {len(networks)} adet")
        return networks

    def find_network_path(self, network_name: str) -> Optional[str]:
        """
        Network adının tam yolunu bulur (package.NetworkName formatında).
        """
        examples_dir = os.path.join(self.working_dir, "examples")
        src_dir = os.path.join(self.working_dir, "src")
        
        search_dirs = [examples_dir, src_dir]
        
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
            
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    if file.endswith(".ned"):
                        file_path = os.path.join(root, file)
                        try:
                            encodings = ['utf-8', 'latin-1', 'cp1252']
                            content = None
                            
                            for enc in encodings:
                                try:
                                    with open(file_path, 'r', encoding=enc) as f:
                                        content = f.read()
                                    break
                                except (UnicodeDecodeError, UnicodeError):
                                    continue
                            
                            if content is None:
                                continue
                            
                            # Network tanımını bul
                            if re.search(rf'\bnetwork\s+{re.escape(network_name)}\b', content):
                                # Package ismini bul
                                pkg_match = re.search(r'\bpackage\s+([\w\.]+);', content)
                                if pkg_match:
                                    full_name = f"{pkg_match.group(1)}.{network_name}"
                                    logger.info(f"Network bulundu: {network_name} -> {full_name}")
                                    return full_name
                                return network_name
                        except Exception as e:
                            continue
        
        logger.warning(f"Network yolu bulunamadı: {network_name}")
        return None