import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QComboBox, 
                           QFileDialog, QTextEdit, QLineEdit)

class DataAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Lab6')
        self.setGeometry(100, 100, 1200, 800)
      
        self.df = None
        
  
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)
        
   
        self.figure = plt.Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        top_layout.addWidget(self.canvas)
        
     
        bottom_panel = QWidget()
        bottom_layout = QHBoxLayout(bottom_panel)
        
      
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        
      
        left_controls = QWidget()
        left_controls_layout = QVBoxLayout(left_controls)
        
       
        self.load_button = QPushButton('Загрузить файл')
        self.load_button.clicked.connect(self.load_data)
        left_controls_layout.addWidget(self.load_button)
        
       
        self.graph_type = QComboBox()
        self.graph_type.addItems(['Линейный график', 'Гистограмма', 'Круговая диаграмма'])
        self.graph_type.currentIndexChanged.connect(self.update_plot)
        left_controls_layout.addWidget(QLabel('Выберите тип графика:'))
        left_controls_layout.addWidget(self.graph_type)
        
        
        middle_controls = QWidget()
        middle_controls_layout = QVBoxLayout(middle_controls)
        
       
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        self.stats_display.setMaximumHeight(150)
        middle_controls_layout.addWidget(QLabel('Статистистика:'))
        middle_controls_layout.addWidget(self.stats_display)
        
        
        right_controls = QWidget()
        right_controls_layout = QVBoxLayout(right_controls)
        
        right_controls_layout.addWidget(QLabel('Добавить новую запись:'))
        
        
        input_fields = QWidget()
        input_layout = QHBoxLayout(input_fields)
        
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText('Date')
        self.value1_input = QLineEdit()
        self.value1_input.setPlaceholderText('Value 1')
        self.value2_input = QLineEdit()
        self.value2_input.setPlaceholderText('Value 2')
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText('Category')
        
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.value1_input)
        input_layout.addWidget(self.value2_input)
        input_layout.addWidget(self.category_input)
        
        right_controls_layout.addWidget(input_fields)
        
        self.add_data_button = QPushButton('Добавить')
        self.add_data_button.clicked.connect(self.add_manual_data)
        right_controls_layout.addWidget(self.add_data_button)
        
      
        controls_layout.addWidget(left_controls)
        controls_layout.addWidget(middle_controls)
        controls_layout.addWidget(right_controls)
        
        bottom_layout.addWidget(controls_widget)
        
       
        layout.addWidget(top_panel, stretch=2)
        layout.addWidget(bottom_panel, stretch=1)

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')
        if filename:
            self.df = pd.read_csv(filename)
            self.update_statistics()
            self.update_plot()

    def update_statistics(self):
        if self.df is not None:
            stats = f"Количество записей: {len(self.df)}\n"
            stats += f"Столбцов: {len(self.df.columns)}\n\n"
            stats += "статистика по данным :\n"
            stats += str(self.df.describe())
            self.stats_display.setText(stats)

    def update_plot(self):
        if self.df is None:
            return
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        plot_type = self.graph_type.currentText()
        
        if plot_type == 'Линейный график':
            ax.plot(pd.to_datetime(self.df['Date']), self.df['Value1'])
            ax.set_xlabel('Date')
            ax.set_ylabel('Value 1')
            ax.tick_params(axis='x', rotation=45)
        
        elif plot_type == 'Гистограмма':
            ax.bar(pd.to_datetime(self.df['Date']), self.df['Value2'])
            ax.set_xlabel('Date')
            ax.set_ylabel('Value 2')
            ax.tick_params(axis='x', rotation=45)
        
        elif plot_type == 'Круговая диаграмма':
            category_counts = self.df['Category'].value_counts()
            ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')
        
        self.figure.tight_layout()
        self.canvas.draw()

    def add_manual_data(self):
        if self.df is None:
            return
        
        try:
            new_data = {
                'Date': [self.date_input.text()],
                'Value1': [float(self.value1_input.text())],
                'Value2': [float(self.value2_input.text())],
                'Category': [self.category_input.text()]
            }
            
            new_row = pd.DataFrame(new_data)
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            
         
            self.date_input.clear()
            self.value1_input.clear()
            self.value2_input.clear()
            self.category_input.clear()
            
        
            self.update_statistics()
            self.update_plot()
            
        except ValueError:
            print("Please enter valid data")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
