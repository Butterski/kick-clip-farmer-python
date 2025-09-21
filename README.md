# 🚀 Kick.com Clip View Bot

A Python-based tool for generating views on Kick.com clips using automated bots. This project includes two versions: one with proxy support and one without.

## 📁 Project Structure

```
kick-clipper/
├── main.py           # Main script with proxy support
├── main_no_proxy.py  # Script without proxy support
├── proxies.txt       # Proxy list file (required for main.py)
└── README.md         # This file
```

## 🔧 Requirements

- Python 3.7+
- `curl_cffi` library

### Installation

```bash
pip install curl-cffi
```

## 📄 Scripts Overview

### 1. `main.py` - Proxy-Enabled Version

**Features:**
- Uses proxy rotation for anonymity
- Auto-calculates bot count based on available proxies (proxies × 5)
- Load balances requests across multiple IP addresses
- Real-time dashboard with comprehensive statistics
- Higher throughput potential

**Requirements:**
- `proxies.txt` file with proxy list

### 2. `main_no_proxy.py` - Direct Connection Version

**Features:**
- Direct connection without proxies
- Manual bot count configuration
- Warning system for rate limiting
- Simplified setup (no proxy configuration needed)
- All requests come from your IP address

**Use Cases:**
- Testing purposes
- When proxies are not available
- Smaller scale operations

## 🚦 Getting Started

### Option 1: Using Proxy Version (Recommended)

1. **Prepare proxy list:**
   Create a `proxies.txt` file with one proxy per line in format:
   ```
   ip:port:username:password
   ip:port:username:password
   ...
   ```

   # **Need proxies?** You can purchase high-quality proxies at [webshare.io](https://www.webshare.io/?referral_code=6aztdbgwxwkf)

2. **Run the script:**
   ```bash
   python main.py
   ```

3. **Follow the prompts:**
   - Enter Kick.com clip URL
   - Enter views per bot
   - Monitor the real-time dashboard

### Option 2: Using No-Proxy Version

1. **Run the script:**
   ```bash
   python main_no_proxy.py
   ```

2. **Follow the prompts:**
   - Enter Kick.com clip URL
   - Enter number of bots (recommended: 5-20)
   - Enter views per bot
   - Confirm to proceed (all requests from your IP)

## 📊 Dashboard Features

Both scripts include a real-time dashboard that displays:

- **Runtime Information:** Current session duration
- **View Statistics:** Current views, initial views, views gained, rate per minute/second
- **Bot Statistics:** Active/finished bots, success/failure rates
- **Progress Tracking:** Visual progress bar towards target views
- **Proxy Information:** Available proxy count (main.py only)

## ⚙️ Configuration

### Proxy Format (main.py)
```
ip:port:username:password
```
Example:
```
192.168.1.100:8080:user1:pass1
10.0.0.50:3128:user2:pass2
```

### Bot Configuration
- **main.py:** Auto-calculated as `proxy_count × 5`
- **main_no_proxy.py:** User-defined (recommended: 5-20)

### Timing Configuration
- **Proxy version:** 2-8 seconds between requests
- **No-proxy version:** 5-15 seconds between requests (longer to avoid rate limiting)

## 🔗 Supported URL Format

Both scripts support Kick.com clip URLs in the format:
```
https://kick.com/CHANNEL/clips/CLIP_ID
```

Example:
```
https://kick.com/streamer123/clips/abc123def456
```

## ⚠️ Important Notes

### Legal and Ethical Considerations
- This tool is for educational purposes only
- Ensure compliance with Kick.com's Terms of Service
- Use responsibly and respect platform guidelines
- Consider the impact on content creators and platform integrity

### Security and Privacy
- **Proxy version:** Distributes requests across multiple IP addresses
- **No-proxy version:** All requests originate from your IP address
- Monitor your network usage and respect rate limits

### Rate Limiting
- **Proxy version:** Less likely to hit rate limits due to IP distribution
- **No-proxy version:** Higher risk of rate limiting from single IP
- Both versions include built-in delays between requests

## 🛠️ Troubleshooting

### Common Issues

1. **"No proxies found" error:**
   - Ensure `proxies.txt` exists and contains valid proxies
   - Check proxy format: `ip:port:username:password`

2. **"Invalid URL format" error:**
   - Verify the clip URL follows the correct format
   - Ensure the URL is a valid Kick.com clip link

3. **Connection timeouts:**
   - Check your internet connection
   - Verify proxy credentials (if using proxy version)
   - Try reducing the number of concurrent bots

4. **High failure rate:**
   - Validate proxy list quality
   - Reduce request frequency
   - Check if target clip still exists

### Performance Optimization

- **Proxy version:** More proxies = better performance and lower detection risk
- **No-proxy version:** Use fewer bots (5-10) to avoid overwhelming your connection
- Monitor success rates and adjust bot count accordingly

## 📈 Best Practices

1. **Start Small:** Begin with fewer bots and gradually increase
2. **Monitor Performance:** Watch success rates and adjust accordingly
3. **Respect Limits:** Don't overwhelm the target server
4. **Use Quality Proxies:** Better proxies = better success rates
5. **Test First:** Use the no-proxy version for initial testing

## 🔄 Updates and Maintenance

- Regularly update proxy lists for optimal performance
- Monitor script output for any errors or warnings
- Keep the `curl_cffi` library updated
- Check Kick.com's Terms of Service for any changes

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all requirements are met
3. Ensure proper file formats and configurations
4. Monitor console output for specific error messages

---

**Disclaimer:** This tool is provided for educational purposes only. Users are responsible for ensuring compliance with all applicable terms of service and laws. Use at your own risk.