import threading
import time
import random
import re
import os
from datetime import datetime
from curl_cffi import requests

# Global tracking variables
bot_stats = {}
total_successful_views = 0
start_time = None
initial_views = 0
stats_lock = threading.Lock()

def load_proxies(file_path="proxies.txt"):
    """Load proxies from file"""
    try:
        with open(file_path, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            print(f"❌ No proxies found in '{file_path}'")
            return []
        print(f"✅ Loaded {len(proxies)} proxies")
        return proxies
    except FileNotFoundError:
        print(f"❌ Proxy file '{file_path}' not found")
        return []
    except Exception as e:
        print(f"❌ Error loading proxies: {e}")
        return []

def parse_clip_url(url):
    """Extract channel name and clip ID from Kick.com clip URL"""
    # Pattern: https://kick.com/CHANNEL/clips/CLIP_ID
    pattern = r"https://kick\.com/([^/]+)/clips/([^/\?]+)"
    match = re.search(pattern, url)
    
    if match:
        channel_name = match.group(1)
        clip_id = match.group(2)
        return channel_name, clip_id
    else:
        print(f"❌ Invalid Kick.com clip URL format: {url}")
        print("💡 Expected format: https://kick.com/CHANNEL/clips/CLIP_ID")
        return None, None

def get_random_proxy(proxies_list):
    """Get a random proxy from the list"""
    if not proxies_list:
        return None
    
    proxy = random.choice(proxies_list)
    try:
        ip, port, user, pwd = proxy.split(":")
        proxy_url = f"http://{user}:{pwd}@{ip}:{port}"
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        return proxy_dict
    except ValueError:
        print(f"❌ Invalid proxy format: {proxy} (expected ip:port:user:pass)")
        return None

def get_clip_views(clip_id, proxies_list):
    """Fetch current clip views from Kick.com API"""
    for _ in range(3):  # Try up to 3 times
        try:
            proxy_dict = get_random_proxy(proxies_list)
            session = requests.Session(impersonate="firefox135")
            if proxy_dict:
                session.proxies = proxy_dict
            session.timeout = 10
            
            response = session.get(f"https://kick.com/api/v2/clips/{clip_id}")
            if response.status_code == 200:
                data = response.json()
                return data.get("clip", {}).get("view_count", 0)
        except Exception:
            continue
    return None

def simulate_view(clip_url, channel_name, clip_id, proxies_list, bot_id, views_per_bot):
    """Simulate views for a clip using a single bot"""
    global total_successful_views, bot_stats
    
    # Initialize bot stats
    with stats_lock:
        bot_stats[bot_id] = {"successful": 0, "failed": 0, "status": "Starting..."}
    
    successful_views = 0
    failed_views = 0
    
    for view_num in range(1, views_per_bot + 1):
        try:
            # Update bot status
            with stats_lock:
                bot_stats[bot_id]["status"] = f"View {view_num}/{views_per_bot}"
            
            # Get random proxy
            proxy_dict = get_random_proxy(proxies_list)
            if not proxy_dict:
                failed_views += 1
                with stats_lock:
                    bot_stats[bot_id]["failed"] = failed_views
                time.sleep(2)
                continue
            
            # Create session with random user agent
            session = requests.Session(impersonate="firefox135")
            session.proxies = proxy_dict
            session.timeout = 15
            
            # Random user agents for variety
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            
            session.headers.update({
                "User-Agent": random.choice(user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none"
            })
            
            # Make request to clip page (this should register a view)
            response = session.get(clip_url)
            
            if response.status_code == 200:
                successful_views += 1
                with stats_lock:
                    total_successful_views += 1
                    bot_stats[bot_id]["successful"] = successful_views
            else:
                failed_views += 1
                with stats_lock:
                    bot_stats[bot_id]["failed"] = failed_views
            
            # Random delay between requests (2-8 seconds)
            delay = random.randint(2, 8)
            time.sleep(delay)
            
        except Exception as e:
            failed_views += 1
            with stats_lock:
                bot_stats[bot_id]["failed"] = failed_views
            time.sleep(3)
    
    # Mark bot as finished
    with stats_lock:
        bot_stats[bot_id]["status"] = "Finished"
    
    return successful_views

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_dashboard(clip_id, proxies_list, target_views, num_bots):
    """Display real-time dashboard"""
    global start_time, initial_views, bot_stats, total_successful_views
    
    while True:
        try:
            clear_screen()
            
            # Get current clip views
            current_views = get_clip_views(clip_id, proxies_list)
            
            # Calculate runtime
            runtime = time.time() - start_time if start_time else 0
            hours, remainder = divmod(int(runtime), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # Calculate views gained
            views_gained = current_views - initial_views if current_views and initial_views else 0
            
            # Calculate rates
            views_per_second = views_gained / runtime if runtime > 0 else 0
            views_per_minute = views_per_second * 60
            
            # Bot statistics
            active_bots = 0
            finished_bots = 0
            total_bot_success = 0
            total_bot_failed = 0
            
            with stats_lock:
                for bot_id, stats in bot_stats.items():
                    total_bot_success += stats["successful"]
                    total_bot_failed += stats["failed"]
                    if stats["status"] == "Finished":
                        finished_bots += 1
                    else:
                        active_bots += 1
            
            # Dashboard display
            print("🚀 KICK.COM CLIP VIEW BOT DASHBOARD 🚀")
            print("=" * 60)
            print(f"📎 Clip ID: {clip_id}")
            print(f"⏱️  Runtime: {hours:02d}:{minutes:02d}:{seconds:02d}")
            print("=" * 60)
            
            print("📊 VIEW STATISTICS:")
            if current_views is not None:
                print(f"   Current Views: {current_views:,}")
                print(f"   Initial Views: {initial_views:,}")
                print(f"   Views Gained:  {views_gained:,} (+{views_gained})")
                print(f"   Rate: {views_per_minute:.1f}/min ({views_per_second:.2f}/sec)")
            else:
                print("   Current Views: Unable to fetch")
            
            print("\n🤖 BOT STATISTICS:")
            print(f"   Total Bots: {num_bots}")
            print(f"   Active: {active_bots} | Finished: {finished_bots}")
            print(f"   Bot Success: {total_bot_success:,}")
            print(f"   Bot Failed: {total_bot_failed:,}")
            print(f"   Success Rate: {(total_bot_success/(total_bot_success+total_bot_failed)*100) if (total_bot_success+total_bot_failed) > 0 else 0:.1f}%")
            
            print("\n🎯 PROGRESS:")
            progress = (total_bot_success / target_views * 100) if target_views > 0 else 0
            progress_bar = "█" * int(progress // 2) + "░" * (50 - int(progress // 2))
            print(f"   Target: {target_views:,} views")
            print(f"   Progress: [{progress_bar}] {progress:.1f}%")
            
            print("\n🌐 PROXY INFO:")
            print(f"   Available Proxies: {len(proxies_list)}")
            
            if finished_bots == num_bots:
                print("\n🏁 ALL BOTS FINISHED!")
                break
                
            print("\n⏹️  Press Ctrl+C to stop")
            print("=" * 60)
            
            time.sleep(5)  # Update every 5 seconds
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Dashboard error: {e}")
            time.sleep(5)

def main():
    global start_time, initial_views, bot_stats
    
    print("🚀 KICK.COM CLIP VIEW BOT")
    print("=" * 40)
    
    # Get clip URL from user
    clip_url = input("📎 Enter Kick.com clip URL: ").strip()
    
    # Parse the URL
    channel_name, clip_id = parse_clip_url(clip_url)
    if not channel_name or not clip_id:
        return
    
    print(f"✅ Channel: {channel_name}")
    print(f"✅ Clip ID: {clip_id}")
    
    # Load proxies
    proxies_list = load_proxies()
    if not proxies_list:
        print("❌ Cannot proceed without proxies. Please add proxies to 'proxies.txt'")
        return
    
    # Auto-calculate bot count based on proxies (proxy count * 5)
    auto_bots = len(proxies_list) * 5
    print(f"🤖 Auto-calculated bots: {auto_bots} (proxies × 5)")
    
    # Get number of bots from user with auto-calculated default
    try:
        bot_input = input(f"🤖 Number of bots (press Enter for {auto_bots}): ").strip()
        num_bots = int(bot_input) if bot_input else auto_bots
        
        if num_bots > auto_bots:
            print(f"⚠️  Warning: {num_bots} bots with {len(proxies_list)} proxies may cause issues.")
            confirm = input("Continue anyway? (y/N): ").strip().lower()
            if confirm != 'y':
                num_bots = auto_bots
                print(f"🔄 Using recommended {auto_bots} bots instead.")
        
    except ValueError:
        print("❌ Invalid input. Using auto-calculated value.")
        num_bots = auto_bots
    
    print(f"✅ Using {num_bots} bots")
    
    # Get views per bot from user
    try:
        views_per_bot = int(input("👁️  Views per bot: "))
    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")
        return
    
    target_views = num_bots * views_per_bot
    print(f"🎯 Target total views: {target_views:,}")
    print("=" * 40)
    
    # Get initial clip views
    print("📊 Getting initial clip views...")
    initial_views = get_clip_views(clip_id, proxies_list)
    if initial_views is not None:
        print(f"📈 Initial views: {initial_views:,}")
    else:
        print("⚠️  Could not fetch initial views")
        initial_views = 0
    
    print("🔥 Starting view bot army...")
    print("=" * 40)
    
    # Start threads
    threads = []
    start_time = time.time()
    
    for i in range(num_bots):
        thread = threading.Thread(
            target=simulate_view,
            args=(clip_url, channel_name, clip_id, proxies_list, i+1, views_per_bot),
            daemon=True
        )
        threads.append(thread)
        thread.start()
        
        # Small delay between starting threads
        time.sleep(0.05)
    
    print(f"✅ All {num_bots} bots started!")
    time.sleep(2)
    
    # Start dashboard in main thread
    try:
        display_dashboard(clip_id, proxies_list, target_views, num_bots)
    except KeyboardInterrupt:
        print("\n🛑 STOPPING BOTS...")
        print("⏳ Waiting for current requests to finish...")
        time.sleep(3)
        print("✅ Bot army stopped!")

if __name__ == "__main__":
    main()