import webbrowser

from PySide2.QtCore import QCoreApplication, QTimer
from PySide2.QtGui import QClipboard
from PySide2.QtWidgets import QMenu, QSystemTrayIcon

from .manage_lnd.lnd_manager_tabs_dialog import LndManagerTabsDialog
from .manage_lnd.zap_qrcode_label import ZapQrcodeLabel
from .manage_bitcoind import BitcoindManagerTabsDialog
from node_launcher.gui.utilities import reveal
from node_launcher.node_set import NodeSet


class Menu(QMenu):
    def __init__(self, node_set: NodeSet, system_tray):
        super().__init__()
        self.node_set = node_set
        self.system_tray = system_tray

        # Bitcoind
        self.bitcoind_status_action = self.addAction('bitcoind off')
        self.bitcoind_status_action.setEnabled(False)
        self.node_set.bitcoind_node.process.status.connect(
            lambda line: self.bitcoind_status_action.setText(line)
        )

        self.bitcoind_manager_tabs_dialog = BitcoindManagerTabsDialog(
            bitcoind_node=self.node_set.bitcoind_node,
            system_tray=self.system_tray
        )
        self.bitcoin_manage_action = self.addAction('Manage Bitcoind')
        self.bitcoin_manage_action.triggered.connect(
            self.bitcoind_manager_tabs_dialog.show
        )
        self.addSeparator()

        # LND
        self.lnd_status_action = self.addAction('lnd off')
        self.lnd_status_action.setEnabled(False)
        self.node_set.lnd_node.process.status.connect(
            lambda line: self.lnd_status_action.setText(line)
        )

        self.lnd_manager_tabs_dialog = LndManagerTabsDialog(
            lnd_node=self.node_set.lnd_node,
            system_tray=self.system_tray
        )
        self.lnd_manage_action = self.addAction('Manage LND')
        self.lnd_manage_action.triggered.connect(
            self.lnd_manager_tabs_dialog.show
        )

        self.addSeparator()

        # Joule
        self.joule_status_action = self.addAction('Joule Browser UI')
        self.joule_status_action.setEnabled(False)
        self.joule_url_action = self.addAction('Copy Node URL (REST)')
        self.joule_macaroons_action = self.addAction('Show Macaroons')
        self.joule_url_action.triggered.connect(self.copy_rest_url)
        self.joule_macaroons_action.triggered.connect(self.reveal_macaroon_path)

        self.addSeparator()

        # Zap
        self.zap_status_action = self.addAction('Zap Desktop UI')
        self.zap_status_action.setEnabled(False)
        self.zap_open_action = self.addAction('Open Zap Desktop')
        self.zap_open_action.triggered.connect(
            lambda: webbrowser.open(self.node_set.lnd_node.lndconnect_url)
        )
        self.zap_qr_code_label = ZapQrcodeLabel(
            configuration=self.node_set.lnd_node.configuration
        )
        self.show_zap_qrcode_action = self.addAction('Pair Zap Mobile')
        self.show_zap_qrcode_action.triggered.connect(
            self.zap_qr_code_label.show
        )

        self.addSeparator()

        # Quit
        self.quit_action = self.addAction('Quit')
        self.quit_action.triggered.connect(
            lambda _: QCoreApplication.exit(0)
        )

    def copy_rest_url(self):
        QClipboard().setText(self.node_set.lnd_node.configuration.rest_url)

    def reveal_macaroon_path(self):
        reveal(self.node_set.lnd_node.configuration.macaroon_path)
