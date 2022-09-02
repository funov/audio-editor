from model.audio_editor import AudioEditor
from model.files_utils import replace_with_rename
from model.time_utils import (
    to_str_time,
    from_str_time_to_int_seconds,
    get_file_name
)

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


IS_DEBUG = False


class GlueAudioWorker(QRunnable):
    def __init__(self, input_audio_paths, output_audio_path):
        super(GlueAudioWorker, self).__init__()
        self.input_audio_paths = input_audio_paths
        self.output_audio_path = output_audio_path
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.glue_audio(
            self.input_audio_paths,
            self.output_audio_path,
            IS_DEBUG
        )
        self.signals.finished.emit()


class CropAudioWorker(QRunnable):
    def __init__(
            self,
            input_audio_path,
            output_audio_path,
            start_time,
            end_time
    ):
        super(CropAudioWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.start_time = start_time
        self.end_time = end_time
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            AudioEditor.crop_audio(
                self.input_audio_path,
                self.output_audio_path,
                self.start_time,
                self.end_time,
                IS_DEBUG
            )
        except ValueError:
            self.signals.error.emit()
            return
        self.signals.finished.emit()


class PasteAudioWorker(QRunnable):
    def __init__(
            self,
            target_audio_path,
            input_audio_path,
            output_audio_path,
            paste_time
    ):
        super(PasteAudioWorker, self).__init__()
        self.target_audio_path = target_audio_path
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.paste_time = paste_time
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            AudioEditor.paste_audio(
                self.target_audio_path,
                self.input_audio_path,
                self.output_audio_path,
                self.paste_time,
                IS_DEBUG
            )
        except ValueError:
            self.signals.error.emit()
            return
        self.signals.finished.emit()


class ReverseAudioWorker(QRunnable):
    def __init__(
            self,
            input_audio_path,
            output_audio_path,
            start_s=None,
            start_m=None,
            start_h=None,
            duration_s=None,
            duration_m=None,
            duration_h=None
    ):
        super(ReverseAudioWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.start_s = start_s
        self.start_m = start_m
        self.start_h = start_h
        self.duration_s = duration_s
        self.duration_m = duration_m
        self.duration_h = duration_h
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.reverse_fragment_audio(
            self.input_audio_path,
            self.output_audio_path,
            self.start_s,
            self.start_m,
            self.start_h,
            self.duration_s,
            self.duration_m,
            self.duration_h,
            IS_DEBUG
        )
        self.signals.finished.emit()


class ChangeSpeedWorker(QRunnable):
    def __init__(
            self,
            input_audio_path,
            output_audio_path,
            speed,
            start_s=None,
            start_m=None,
            start_h=None,
            duration_s=None,
            duration_m=None,
            duration_h=None
    ):
        super(ChangeSpeedWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.speed = speed
        self.start_s = start_s
        self.start_m = start_m
        self.start_h = start_h
        self.duration_s = duration_s,
        self.duration_m = duration_m
        self.duration_h = duration_h
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.change_fragment_speed(
            self.input_audio_path,
            self.output_audio_path,
            self.speed,
            self.start_s,
            self.start_m,
            self.start_h,
            self.duration_s,
            self.duration_m,
            self.duration_h,
            IS_DEBUG
        )
        self.signals.finished.emit()


class ChangeVolumeWorker(QRunnable):
    def __init__(
            self,
            input_audio_path,
            output_audio_path,
            volume,
            start_s=None,
            start_m=None,
            start_h=None,
            duration_s=None,
            duration_m=None,
            duration_h=None
    ):
        super(ChangeVolumeWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.volume = volume
        self.start_s = start_s
        self.start_m = start_m
        self.start_h = start_h
        self.duration_s = duration_s,
        self.duration_m = duration_m
        self.duration_h = duration_h
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.change_fragment_volume(
            self.input_audio_path,
            self.output_audio_path,
            self.volume,
            self.start_s,
            self.start_m,
            self.start_h,
            self.duration_s,
            self.duration_m,
            self.duration_h,
            IS_DEBUG
        )
        self.signals.finished.emit()


class ConvertAudioWorker(QRunnable):
    def __init__(self, input_audio_path, output_audio_path):
        super(ConvertAudioWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        AudioEditor.convert(
            self.input_audio_path,
            self.output_audio_path,
            IS_DEBUG
        )
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


class Utils:
    @staticmethod
    def replace_with_rename(source, destination_folder, new_name=None):
        return replace_with_rename(source, destination_folder, new_name)

    @staticmethod
    def to_str_time(seconds, minutes, hours):
        return to_str_time(seconds, minutes, hours)

    @staticmethod
    def from_str_time_to_int_seconds(str_time):
        return from_str_time_to_int_seconds(str_time)

    @staticmethod
    def get_file_name():
        return get_file_name()


class WorkerSignals(QObject):
    result = pyqtSignal(object)
    finished = pyqtSignal()
    error = pyqtSignal()
