import subprocess
import time
import zmq

TRACK = r"D:\Share\Music\Dance MIX  - 130 BPM\Dance MIX  - 130 BPM.mp3"
ADDRESS = "tcp://127.0.0.1:5555"

process = subprocess.Popen(
    [
        "ffmpeg",
        "-re",
        "-i", TRACK,
        "-af",
        "volume@vol=1.0,azmq=bind_address=" + ADDRESS,
        "-f",
        "null",
        "-"
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

time.sleep(2)

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(ADDRESS)

print("FFmpeg запущен.")
print("Отправляем громкость 0.2...")

socket.send_string("vol volume 0.2")
print("Ответ:", socket.recv_string())

time.sleep(3)

print("Отправляем громкость 1.0...")

socket.send_string("vol volume 1.0")
print("Ответ:", socket.recv_string())

time.sleep(3)

print("Останавливаем тест.")

process.terminate()
process.wait()

socket.close()
context.term()

