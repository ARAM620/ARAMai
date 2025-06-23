# system_command.py
import os

def handle_system_command(target):
    target = target.strip()
    if "종료" in target:
        print("[시스템 명령] 컴퓨터 종료 중...")
        os.system("shutdown /s /t 5")  # 5초 후 종료
        return True
    elif "재시작" in target:
        print("[시스템 명령] 컴퓨터 재시작 중...")
        os.system("shutdown /r /t 5")  # 5초 후 재시작
        return True
    elif "절전" in target or "대기" in target:
        print("[시스템 명령] 절전 모드로 전환 중...")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return True
    else:
        print(f"[시스템 명령] '{target}' 명령을 이해하지 못했습니다.")
        return False
