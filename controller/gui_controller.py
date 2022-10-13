from model.audio_editor import AudioEditor
from model.files_utils import replace_with_rename
from model.time_utils import (
    to_str_time,
    from_str_time_to_int_seconds,
    get_file_name
)

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class GlueAudioWorker(QRunnable):
    def __init__(self, input_audio_paths, output_audio_path, is_debug):
        super(GlueAudioWorker, self).__init__()
        self.input_audio_paths = input_audio_paths
        self.output_audio_path = output_audio_path
        self.signals = WorkerSignals()
        self.is_debug = is_debug

    @pyqtSlot()
    def run(self):
        AudioEditor.glue_audio(
            self.input_audio_paths,
            self.output_audio_path,
            self.is_debug
        )
        self.signals.finished.emit()


class CropAudioWorker(QRunnable):
    def __init__(
            self,
            input_audio_path,
            output_audio_path,
            start_time,
            end_time,
            is_debug
    ):
        super(CropAudioWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.start_time = start_time
        self.end_time = end_time
        self.is_debug = is_debug
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            AudioEditor.crop_audio(
                self.input_audio_path,
                self.output_audio_path,
                self.start_time,
                self.end_time,
                self.is_debug
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
            paste_time,
            is_debug
    ):
        super(PasteAudioWorker, self).__init__()
        self.target_audio_path = target_audio_path
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.paste_time = paste_time
        self.is_debug = is_debug
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            AudioEditor.paste_audio(
                self.target_audio_path,
                self.input_audio_path,
                self.output_audio_path,
                self.paste_time,
                self.is_debug
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
            start_time,
            end_time,
            is_debug
    ):
        super(ReverseAudioWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.start_time = start_time
        self.end_time = end_time
        self.is_debug = is_debug
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            AudioEditor.reverse_fragment_audio(
                self.input_audio_path,
                self.output_audio_path,
                self.start_time,
                self.end_time,
                self.is_debug
            )
        except ValueError:
            self.signals.error.emit()
            return
        self.signals.finished.emit()


class ChangeSpeedWorker(QRunnable):
    def __init__(
            self,
            input_audio_path,
            output_audio_path,
            speed,
            start_time,
            end_time,
            is_debug
    ):
        super(ChangeSpeedWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.speed = speed
        self.start_time = start_time
        self.end_time = end_time
        self.signals = WorkerSignals()
        self.is_debug = is_debug

    @pyqtSlot()
    def run(self):
        try:
            AudioEditor.change_fragment_speed(
                self.input_audio_path,
                self.output_audio_path,
                self.speed,
                self.start_time,
                self.end_time,
                self.is_debug
            )
        except ValueError:
            self.signals.error.emit()
            return
        self.signals.finished.emit()


class ChangeVolumeWorker(QRunnable):
    def __init__(
            self,
            input_audio_path,
            output_audio_path,
            volume,
            start_time,
            end_time,
            is_debug
    ):
        super(ChangeVolumeWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.volume = volume
        self.start_time = start_time
        self.end_time = end_time
        self.is_debug = is_debug
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            AudioEditor.change_fragment_volume(
                self.input_audio_path,
                self.output_audio_path,
                self.volume,
                self.start_time,
                self.end_time,
                self.is_debug
            )
        except ValueError:
            self.signals.error.emit()
            return
        self.signals.finished.emit()


class ConvertAudioWorker(QRunnable):
    def __init__(self, input_audio_path, output_audio_path, is_debug):
        super(ConvertAudioWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.signals = WorkerSignals()
        self.is_debug = is_debug

    @pyqtSlot()
    def run(self):
        AudioEditor.convert(
            self.input_audio_path,
            self.output_audio_path,
            self.is_debug
        )
        self.signals.finished.emit()


class GetAudioInfoWorker(QRunnable):
    def __init__(self, path, is_debug):
        super(GetAudioInfoWorker, self).__init__()
        self.path = path
        self.signals = WorkerSignals()
        self.is_debug = is_debug

    @pyqtSlot()
    def run(self):
        audio_info = AudioEditor.get_audio_info(self.path, self.is_debug)
        self.signals.result.emit(audio_info)


class GetSpectrogramWorker(QRunnable):
    def __init__(self, input_audio_path, output_picture_path, is_debug):
        super(GetSpectrogramWorker, self).__init__()
        self.input_audio_path = input_audio_path
        self.output_picture_path = output_picture_path
        self.signals = WorkerSignals()
        self.is_debug = is_debug

    @pyqtSlot()
    def run(self):
        AudioEditor.get_spectrogram(
            self.input_audio_path,
            self.output_picture_path,
            self.is_debug
        )
        self.signals.finished.emit()


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
