# Nitrogen Campaign

#### Scenario :

A well-coordinated attack unfolded when a corporate employee inadvertently downloaded a fake **Advanced IP Scanner** from a compromised website, providing the attacker with initial access.

Using stealthy techniques, the adversary deployed multiple **C2 (Command and Control) beacons** to maintain persistence, moved laterally through the network using stolen credentials, and methodically escalated privileges. After days of reconnaissance and data exfiltration, the attack culminated in a domain-wide deployment of **BlackCat ransomware**, encrypting critical systems in a synchronized strike.

Your Task Perform a thorough analysis of the malicious executable to identify its components, uncover its behavior, and determine the extent of the compromise.

#### Category:  
Malware Analysis

#### Tactics:
Execution - Command and Control  - Defense Evasion - Persistence - Privilege Escalation - Lateral Movement - Exfiltration - Impact

#### Tools:
IDA - CyberChef -Process Monitor - Process Hacker - Autoruns - Wireshark

# Challenge Files :

Version.zip contained mainly:
	- setup.exe (Advanced IP Scanner executable)
	- two hidden Python DLLs (python311.dll & python311x.dll)
	- service_probes.aes
	- important.txt

# walkthrough :

- version.zip
	- setup.exe
	- python311.dll
		- decrypts an AES-encrypted 'service_probes.aes'
	- python311x.dll
		- Discover.bat & 1.bat & up.bat & Tools.bat & Discover.bat
	- service_probes.aes
		- pycryptodome.bat &  & data.aes
		- slv.py
			- decrypts an AES-encrypted 'data.aes' and execute 'pythonw.exe'
		- pythonw.exe
			- worksliv.py & wo14.py & wo12.py 
			- example.exe
				- RECOVER-wragz12-FILES.txt & UpdateEdge.bat & example.py
