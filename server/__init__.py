from flask import Flask
from . import config
app = Flask(__name__)


from .utils import eval
from .utils.dataset import array2dcm
from .utils.upload import upload
from .utils.dataset.convert import Convertion

cnv = Convertion(config.NPYDIR)
