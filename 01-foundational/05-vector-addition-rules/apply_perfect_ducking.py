import wave
import numpy as np
import subprocess

MUSIC_IN = "music_looped.wav"
MUSIC_OUT = "music_perfect_ducked.wav"
VOICE_IN = "audio.wav"
VIDEO_IN = "video_only.mp4"
FINAL_VIDEO = "Episode_05_Complete.mp4"

# 1) المستويات
VOL_INTRO = 0.95      # رفع مستوى الإنترو لتعويض هدوء بداية التراك الأصلي
VOL_LOUD = 0.65       # صوت الموسيقى في الأوترو وكروت الفصول
VOL_BG = 0.075        # صوت الخلفية الهادي أثناء الشرح

CHAPTER_STARTS = [
    129.083,   # الفصل 2
    220.583,   # الفصل 3
    488.100,   # الفصل 4
    716.783,   # الفصل 5
    919.500,   # الفصل 6
    1065.283,  # الفصل 7
    1214.567,  # الفصل 8
    1339.867,  # الفصل 9
    1511.133,  # الفصل 10
    1760.333,  # الفصل 11
]
OUTRO_START = 1819.133
TOTAL_DUR = 1824.133

kf_times = []
kf_vols = []

def add_kf(t, v):
    kf_times.append(float(t))
    kf_vols.append(float(v))

# 1) الإنترو: عالي وقوي في أول 7 ثوانٍ، وينزل تدريجياً ليستقر قبل كلام الفصل الأول
add_kf(0.0, VOL_INTRO)
add_kf(7.0, VOL_INTRO)
add_kf(8.8, VOL_LOUD)
add_kf(9.6, VOL_BG)

# 2) الفواصل بين الفصول
for Tk in CHAPTER_STARTS:
    if abs(Tk - 1511.133) < 0.1:
        # فاصل الانتقال من المشهد 9 إلى 10 (مرحل للأمام بعد انتهاء كلام المشهد التاسع)
        add_kf(Tk + 0.3, VOL_BG)
        add_kf(Tk + 1.0, VOL_LOUD)
        add_kf(Tk + 3.8, VOL_LOUD)
        add_kf(Tk + 4.6, VOL_BG)
    else:
        add_kf(Tk - 0.7, VOL_BG)
        add_kf(Tk - 0.1, VOL_LOUD)
        add_kf(Tk + 2.9, VOL_LOUD)
        add_kf(Tk + 3.7, VOL_BG)

# 3) الأوترو
add_kf(OUTRO_START - 0.8, VOL_BG)
add_kf(OUTRO_START, VOL_LOUD)
add_kf(TOTAL_DUR, VOL_LOUD)

print("1) تطبيق رفع صوت الإنترو وتعديل المنحنى...")
with wave.open(MUSIC_IN, 'rb') as wf:
    params = wf.getparams()
    n_channels = params.nchannels
    framerate = params.framerate
    n_frames = params.nframes
    raw_data = wf.readframes(n_frames)

samples = np.frombuffer(raw_data, dtype=np.int16).reshape(-1, n_channels).astype(np.float32)

time_axis = np.linspace(0.0, float(n_frames) / framerate, n_frames, endpoint=False, dtype=np.float32)
envelope = np.interp(time_axis, kf_times, kf_vols).astype(np.float32)

samples[:, 0] *= envelope
samples[:, 1] *= envelope
samples = np.clip(samples, -32768, 32767).astype(np.int16)

with wave.open(MUSIC_OUT, 'wb') as wf:
    wf.setparams(params)
    wf.writeframes(samples.tobytes())

print("2) دمج الفيديو النهائي 4K...")
cmd = [
    "ffmpeg", "-y",
    "-i", VIDEO_IN,
    "-i", VOICE_IN,
    "-i", MUSIC_OUT,
    "-filter_complex",
    "[1:a]adelay=7000|7000,volume=1.0[voice];"
    "[2:a]aformat=sample_rates=48000:channel_layouts=stereo[music];"
    "[voice][music]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]",
    "-map", "0:v",
    "-map", "[aout]",
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-movflags", "+faststart",
    FINAL_VIDEO
]
subprocess.run(cmd, check=True)
print("\n تم الانتهاء بنجاح! اسمع أول 10 ثوانٍ الآن.")