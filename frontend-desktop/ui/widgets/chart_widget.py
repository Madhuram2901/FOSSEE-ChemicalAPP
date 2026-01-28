"""
Chart Widget - Displays matplotlib charts
"""
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ChartWidget(QFrame):
    """Widget for displaying charts using matplotlib"""
    
    def __init__(self, title: str, parent=None):
        """
        Initialize chart widget
        
        Args:
            title: Title of the chart
            parent: Parent widget
        """
        super().__init__(parent)
        self.title = title
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Panel styling
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            ChartWidget {
                background-color: #CDB885;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }
        """)
        self.setMaximumHeight(400)  # Limit chart height
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 10, 12, 5)  # Reduced bottom margin to 0
        layout.setSpacing(6)  # Reduced spacing from 8 to 6
        
        # Title
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(11)  # Reduced from 13
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #111827;")
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(6.5, 3.5), dpi=90)  # Larger figure
        self.figure.patch.set_facecolor('#CDB885')
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(title_label)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
    
    def plot_bar_chart(self, data: dict):
        """
        Plot a bar chart for averages
        
        Args:
            data: Dictionary with averages (flowrate, pressure, temperature)
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Data
        categories = ['Flowrate\n(m³/h)', 'Pressure\n(bar)', 'Temperature\n(°C)']
        values = [
            data['averages']['flowrate'],
            data['averages']['pressure'],
            data['averages']['temperature']
        ]
        colors = ['#3b82f6', '#10b981', '#f59e0b']
        
        # Create bar chart
        bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Styling
        ax.set_ylabel('Value', fontsize=9, fontweight='bold')
        ax.set_title('Average Parameters', fontsize=10, fontweight='bold', pad=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_pie_chart(self, type_distribution: dict):
        """
        Plot a pie chart for equipment type distribution
        
        Args:
            type_distribution: Dictionary with equipment types and counts
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Data
        labels = list(type_distribution.keys())
        sizes = list(type_distribution.values())
        
        # Colors
        colors = plt.cm.Set3(range(len(labels)))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 9}
        )
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        ax.set_title('Equipment Type Distribution', fontsize=10, fontweight='bold', pad=8)
        
        self.figure.tight_layout()
        self.canvas.draw()


class ChartsContainer(QFrame):
    """Container for multiple charts"""
    
    def __init__(self, parent=None):
        """
        Initialize charts container
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)  # Reduced from 16
        
        # Create chart widgets
        self.averages_chart = ChartWidget("Parameter Averages")
        self.distribution_chart = ChartWidget("Type Distribution")
        
        layout.addWidget(self.averages_chart)
        layout.addWidget(self.distribution_chart)
        
        self.setLayout(layout)
    
    def update_charts(self, data: dict):
        """
        Update both charts with new data
        
        Args:
            data: Summary data from API
        """
        self.averages_chart.plot_bar_chart(data)
        self.distribution_chart.plot_pie_chart(data['type_distribution'])
