import sys
import os
import glob
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QTextEdit, QLabel, QFileDialog, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont
from ultralytics import YOLO

# --- 백그라운드 작업용 스레드 (GUI 멈춤 방지) ---
class WorkerThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)

    def __init__(self, task_type, path, model_path):
        super().__init__()
        self.task_type = task_type
        self.path = path
        self.model_path = model_path

    def run(self):
        try:
            model = YOLO(self.model_path)
            
            if self.task_type == "image":
                self.log_signal.emit(f"🚀 '{os.path.basename(self.path)}' 폴더 이미지 분석 시작...")
                results = model.predict(source=self.path, conf=0.25, save=True, project="onion_project", name="gui_image_results")
                
                csv_filename = "cell_counts_result.csv"
                with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow(["파일명", "Interphase(간기)", "Prophase(전기)", "Metaphase(중기)", "Anaphase(후기)", "Telophase(말기)", "총합"])
                    for r in results:
                        counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
                        for cls in r.boxes.cls:
                            counts[int(cls)] += 1
                        writer.writerow([os.path.basename(r.path), counts[0], counts[1], counts[2], counts[3], counts[4], sum(counts.values())])
                
                save_dir = results[0].save_dir if results else "알 수 없음"
                self.log_signal.emit(f"✅ 분석 완료! CSV 저장됨: {csv_filename}")
                self.finished_signal.emit(save_dir)

            elif self.task_type == "video":
                self.log_signal.emit(f"🚀 '{os.path.basename(self.path)}' 동영상 추적 분석 시작...")
                results = model.track(source=self.path, conf=0.25, iou=0.5, save=True, project="onion_project", name="gui_video_results")
                save_dir = results[0].save_dir if results else "알 수 없음"
                self.log_signal.emit("✅ 동영상 분석 완료!")
                self.finished_signal.emit(save_dir)

            elif self.task_type == "realtime":
                self.log_signal.emit("🚀 실시간 카메라 분석 시작! (종료하려면 카메라 창에서 'q' 입력)")
                model.predict(source=self.path, show=True, conf=0.25)
                self.log_signal.emit("✅ 카메라 분석 종료.")
                self.finished_signal.emit("")

        except Exception as e:
            self.log_signal.emit(f"❌ 오류 발생: {str(e)}")
            self.finished_signal.emit("")

# --- 메인 GUI 창 ---
class OnionCellApp(QWidget):
    def __init__(self):
        super().__init__()
        self.model_path = self.find_latest_best_pt()
        self.initUI()

    def find_latest_best_pt(self):
        pts = glob.glob("**/*best.pt", recursive=True)
        return max(pts, key=os.path.getmtime) if pts else None

    def initUI(self):
        self.setWindowTitle('양파 체세포 분열 분석기 (YOLOv11)')
        self.resize(500, 400)
        layout = QVBoxLayout()

        # 제목 라벨
        title = QLabel('🔬 양파 체세포 분열 자동 분석 시스템')
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        # 모델 상태 라벨
        model_status = f"✅ 로드된 모델: {self.model_path}" if self.model_path else "❌ 모델(best.pt)을 찾을 수 없습니다!"
        self.lbl_model = QLabel(model_status)
        layout.addWidget(self.lbl_model)

        # 버튼들
        self.btn_image = QPushButton('📁 1. 폴더 선택 및 이미지 일괄 분석 (CSV 저장)')
        self.btn_image.setMinimumHeight(40)
        self.btn_image.clicked.connect(self.run_image_analysis)
        layout.addWidget(self.btn_image)

        self.btn_video = QPushButton('🎬 2. 동영상 파일 선택 및 추적 분석')
        self.btn_video.setMinimumHeight(40)
        self.btn_video.clicked.connect(self.run_video_analysis)
        layout.addWidget(self.btn_video)

        self.btn_cam = QPushButton('📷 3. 실시간 웹캠/현미경 분석 시작')
        self.btn_cam.setMinimumHeight(40)
        self.btn_cam.clicked.connect(self.run_realtime_analysis)
        layout.addWidget(self.btn_cam)

        # 로그 출력창
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

    def log(self, message):
        self.log_box.append(message)

    def check_model(self):
        if not self.model_path:
            QMessageBox.critical(self, "오류", "학습된 모델(best.pt)이 없습니다.")
            return False
        return True

    def start_worker(self, task_type, path):
        self.btn_image.setEnabled(False)
        self.btn_video.setEnabled(False)
        self.btn_cam.setEnabled(False)
        
        self.worker = WorkerThread(task_type, path, self.model_path)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.on_task_finished)
        self.worker.start()

    def on_task_finished(self, save_dir):
        self.btn_image.setEnabled(True)
        self.btn_video.setEnabled(True)
        self.btn_cam.setEnabled(True)
        if save_dir:
            os.system(f"open '{save_dir}'")

    def run_image_analysis(self):
        if not self.check_model(): return
        folder_path = QFileDialog.getExistingDirectory(self, "분석할 이미지가 있는 폴더를 선택하세요")
        if folder_path:
            self.start_worker("image", folder_path)

    def run_video_analysis(self):
        if not self.check_model(): return
        file_path, _ = QFileDialog.getOpenFileName(self, "분석할 동영상 파일을 선택하세요", "", "Video Files (*.mp4 *.avi *.mov)")
        if file_path:
            self.start_worker("video", file_path)

    def run_realtime_analysis(self):
        if not self.check_model(): return
        # 기본 웹캠은 "0", 외부 카메라는 "1" 등을 사용합니다.
        self.start_worker("realtime", "0")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OnionCellApp()
    ex.show()
    sys.exit(app.exec_())
