from model.audio_editor import AudioEditor
from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


IS_DEBUG = False


class ReverseAudioWorker(QRunnable):
    def __init__(self, input_audio_path, output_audio_path):
        super(ReverseAudioWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.reverse_audio(self.input_audio_path, self.output_audio_path, IS_DEBUG)
        self.signals.finished.emit()


class ConvertAudioWorker(QRunnable):
    def __init__(self, input_audio_path, output_audio_path):
        super(ConvertAudioWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.convert(self.input_audio_path, self.output_audio_path, IS_DEBUG)
        self.signals.finished.emit()


class GlueAudioWorker(QRunnable):
    def __init__(self, input_audio_paths, output_audio_path):
        super(GlueAudioWorker, self).__init__()
        self.input_audio_paths = input_audio_paths
        self.output_audio_path = output_audio_path
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.glue_audio(self.input_audio_paths, self.output_audio_path, IS_DEBUG)
        self.signals.finished.emit()


class ChangeSpeedWorker(QRunnable):
    def __init__(self, input_audio_path, output_audio_path, speed):
        super(ChangeSpeedWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.speed = speed
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.change_speed(self.input_audio_path, self.output_audio_path, self.speed, IS_DEBUG)
        self.signals.finished.emit()


class CropAudioWorker(QRunnable):
    def __init__(self, input_audio_path, output_audio_path, start_s, start_m, start_h, duration):
        super(CropAudioWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.start_s = start_s
        self.start_m = start_m
        self.start_h = start_h
        self.duration = duration
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.crop_audio(self.input_audio_path, self.output_audio_path, self.start_s, self.start_m, self.start_h, self.duration, IS_DEBUG)
        self.signals.finished.emit()


class ChangeVolumeWorker(QRunnable):
    def __init__(self, input_audio_path, output_audio_path, volume):
        super(ChangeVolumeWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.volume = volume
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.change_volume(self.input_audio_path, self.output_audio_path, self.volume, IS_DEBUG)
        self.signals.finished.emit()


class GetAudioInfoWorker(QRunnable):
    def __init__(self, path):
        super(GetAudioInfoWorker, self).__init__()
        self.path = path
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        audio_info = AudioEditor.get_audio_info(self.path, IS_DEBUG)
        self.signals.result.emit(audio_info)


class WorkerSignals(QObject):
    result = pyqtSignal(object)
    finished = pyqtSignal()
