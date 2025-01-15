from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, random, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class OpenLoop:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://effapmdildnpkiaeghlkicpfflpiambm",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": FakeUserAgent().random
        }
        self.proxies = []
        self.proxy_index = 0

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Ping {Fore.BLUE + Style.BRIGHT}OpenLoop - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_auto_proxies(self):
        url = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt"
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url) as response:
                    response.raise_for_status()
                    content = await response.text()
                    with open('proxy.txt', 'w') as f:
                        f.write(content)

                    self.proxies = content.splitlines()
                    if not self.proxies:
                        self.log(f"{Fore.RED + Style.BRIGHT}No proxies found in the downloaded list!{Style.RESET_ALL}")
                        return
                    
                    self.log(f"{Fore.GREEN + Style.BRIGHT}Proxies successfully downloaded.{Style.RESET_ALL}")
                    self.log(f"{Fore.YELLOW + Style.BRIGHT}Loaded {len(self.proxies)} proxies.{Style.RESET_ALL}")
                    self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                    await asyncio.sleep(3)
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed to load proxies: {e}{Style.RESET_ALL}")
            return []
        
    async def load_manual_proxy(self):
        try:
            if not os.path.exists('manual_proxy.txt'):
                print(f"{Fore.RED + Style.BRIGHT}Proxy file 'manual_proxy.txt' not found!{Style.RESET_ALL}")
                return

            with open('manual_proxy.txt', "r") as f:
                proxies = f.read().splitlines()

            self.proxies = proxies
            self.log(f"{Fore.YELLOW + Style.BRIGHT}Loaded {len(self.proxies)} proxies.{Style.RESET_ALL}")
            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
            await asyncio.sleep(3)
        except Exception as e:
            print(f"{Fore.RED + Style.BRIGHT}Failed to load manual proxies: {e}{Style.RESET_ALL}")
            self.proxies = []
    
    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        
        return f"http://{proxies}" # Change with yours proxy schemes if your proxy not have schemes [http:// or socks5://]

    def get_next_proxy(self):
        if not self.proxies:
            self.log(f"{Fore.RED + Style.BRIGHT}No proxies available!{Style.RESET_ALL}")
            return None

        proxy = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.check_proxy_schemes(proxy)
    
    def load_accounts(self):
        try:
            if not os.path.exists('accounts.json'):
                self.log(f"{Fore.RED}File 'accounts.json' tidak ditemukan.{Style.RESET_ALL}")
                return

            with open('accounts.json', 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    def hide_email(self, email):
        local, domain = email.split('@', 1)
        hide_local = local[:3] + '*' * 3 + local[-3:]
        return f"{hide_local}@{domain}"
    
    def print_message(self, email: str):
        return self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Status: {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}User Not Found{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}Register First{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
        )
    
    async def renew_token(self, email: str, password: str, proxy=None):
        token = await self.users_login(email, password, proxy)
        if not token:
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Renew Access Token Failed {Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT} Renew Access Token Success {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )
        return token
    
    async def users_login(self, email: str, password: str, proxy=None, retries=3):
        url = "https://api.openloop.so/users/login"
        data = json.dumps({"username":email, "password":password})
        headers = {
            **self.headers,
            "Authorization": "Bearer",
            "Content-Length": str(len(data)),
            "Content-Type": "text/plain;charset=UTF-8",
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 401:
                            return self.print_message(email)
                        
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']['accessToken']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                
                return None
    
    async def users_balance(self, email: str, password: str, token: str, proxy=None, retries=3):
        url = "https://api.openloop.so/bandwidth/info"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        if response.status == 401:
                            token = await self.renew_token(email, password, proxy)
                            headers["Authorization"] = f"Bearer {token}"
                            continue

                        response.raise_for_status()
                        result = await response.json()
                        return result['data']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                
                return None
        
    async def users_mission_list(self, email: str, password: str, token: str, proxy=None, retries=3):
        url = "https://api.openloop.so/missions"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        if response.status == 401:
                            token = await self.renew_token(email, password, proxy)
                            headers["Authorization"] = f"Bearer {token}"
                            continue

                        response.raise_for_status()
                        result = await response.json()
                        return result['data']['missions']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                
                return None
        
    async def users_complete_mission(self, email: str, password: str, token: str, mission_id: int, proxy=None, retries=3):
        url = f"https://api.openloop.so/missions/{mission_id}/complete"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        if response.status == 401:
                            token = await self.renew_token(email, password, proxy)
                            headers["Authorization"] = f"Bearer {token}"
                            continue

                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                
                return None
            
    async def users_send_ping(self, email: str, password: str, token: str, proxy=None, retries=3):
        url = "https://api.openloop.so/bandwidth/share"
        data = json.dumps({"quality":random.randint(60, 100)})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 401:
                            token = await self.renew_token(email, password, proxy)
                            headers["Authorization"] = f"Bearer {token}"
                            continue

                        response.raise_for_status()
                        result = await response.json()
                        return result['data']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                
                return None
            
    async def process_users_earning(self, email: str, password: str, token: str, proxy=None):
        while True:
            balance = await self.users_balance(email, password, token, proxy)
            if balance: 
                today_earning = balance.get('todayEarning', 0)
                total_earning = balance.get('balances', {}).get('POINT', 0)
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Earning: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}Today {today_earning:.2f} PTS{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}Total {total_earning:.2f} PTS{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
                )
            else:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Earning: {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}GET Earning Data Failed{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
                )
            await asyncio.sleep(10 * 60)

    async def process_users_mission(self, email: str, password: str, token: str, proxy=None):
        while True:
            missions = await self.users_mission_list(email, password, token, proxy)
            if missions is not None:
                completed = False
                for mission in missions:
                    mission_id = str(mission['missionId'])
                    title = mission['name']
                    reward = mission['reward']['amount']
                    type = mission['reward']['type']
                    status = mission['status']

                    if mission and status == "available":
                        complete = await self.users_complete_mission(email, password, token, mission_id, proxy)
                        if complete and complete['message'] == 'Success':
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Mission: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{title}{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Reward: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{reward} {type}{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Mission: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{title}{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Isn't Completed {Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        await asyncio.sleep(1)

                    else:
                        completed = True

                if completed:
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} Mission: {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}All Available Mission Is Completed{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Mission: {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}GET Mission Data Failed{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
                )
            await asyncio.sleep(24 * 60 * 60)

    async def process_users_send_ping(self, email: str, password: str, token: str, use_proxy: bool, proxy=None):
        ping_count = 1
        while True:
            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT}Try to Sent Ping...{Style.RESET_ALL}",
                end="\r",
                flush=True
            )

            ping = await self.users_send_ping(email, password, token, proxy)
            if ping:
                today_earning = ping.get('todayEarning', 0)
                total_earning = ping.get('balances', {}).get('POINT', 0)
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT} PING {ping_count} Success {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Earning: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}Today {today_earning} PTS{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}Total {total_earning} PTS{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
                )
            else:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} PING {ping_count} Failed {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                )
                if use_proxy:   
                    proxy = self.get_next_proxy()

            ping_count += 1

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT}Wait For 3 Minutes For Next Ping...{Style.RESET_ALL}",
                end="\r"
            )
            await asyncio.sleep(180)
        
    async def question(self):
        while True:
            try:
                print("1. Run With Auto Proxy")
                print("2. Run With Manual Proxy")
                print("3. Run Without Proxy")
                choose = int(input("Choose [1/2/3] -> ").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Auto Proxy" if choose == 1 else 
                        "With Manual Proxy" if choose == 2 else 
                        "Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Selected.{Style.RESET_ALL}")
                    await asyncio.sleep(1)
                    return choose
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")
            
    async def process_accounts(self, email: str, password: str, use_proxy: bool):
        proxy = None

        if use_proxy:
            proxy = self.get_next_proxy()

        token = None
        while token is None:
            token = await self.users_login(email, password, proxy)
            if not token:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {self.hide_email(email)} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} GET Access Token Failed {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                )
                await asyncio.sleep(1)

                if not use_proxy:
                    return

                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Try With Next Proxy...{Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )

                proxy = self.get_next_proxy()
                continue
            
            await asyncio.gather(
                self.process_users_earning(email, password, token, proxy),
                self.process_users_mission(email, password, token, proxy),
                self.process_users_send_ping(email, password, token, use_proxy, proxy)
            )
    
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED}No accounts loaded from 'accounts.json'.{Style.RESET_ALL}")
                return

            use_proxy_choice = await self.question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )
            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

            if use_proxy and use_proxy_choice == 1:
                await self.load_auto_proxies()
            elif use_proxy and use_proxy_choice == 2:
                await self.load_manual_proxy()
            
            while True:
                tasks = []
                for account in accounts:
                    email = account.get('Email')
                    password = account.get('Password')

                    if email and password:
                        tasks.append(self.process_accounts(email, password, use_proxy))

                await asyncio.gather(*tasks)
                await asyncio.sleep(10)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = OpenLoop()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] OpenLoop - BOT{Style.RESET_ALL}                                       "                              
        )