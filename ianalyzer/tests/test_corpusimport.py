from os import mkdir, rmdir
from os.path import abspath
from shutil import copy
from importlib import reload

import pytest

from ianalyzer import config, corpora

@pytest.fixture(autouse=True)
def configuration(monkeypatch):
    monkeypatch.setattr(config, 'CORPUS', 'times')
    monkeypatch.setattr(config, 'CORPUS_ENDPOINT', 'Times')
    monkeypatch.setattr(config, 'CORPUS_URL', 'Times.index')


def test_key_error(monkeypatch,capsys):
	''' Verify that exception is correctly raised
	- in case the config.CORPORA variable is empty
	'''
	with pytest.raises(KeyError) as e:
		monkeypatch.setattr(config, 'CORPORA', {})
		reload(corpora)
	out, err = capsys.readouterr()
	assert 'No file path for' in str(err)


def test_import_error(monkeypatch,capsys):
	''' Verify that exceptions is correctly raised
	- in case the file path in config.CORPORA is faulty
	'''
	with pytest.raises(FileNotFoundError) as e:
		monkeypatch.setattr(config, 'CORPUS', 'times')
		monkeypatch.setattr(
			config, 'CORPORA', {'times': '/ianalyzer/corpora/tmes.py'}
		)
		reload(corpora)
	out, err = capsys.readouterr()
	assert 'No module describing' in str(err)


def test_import_from_anywhere(monkeypatch, tmpdir):
	''' Verify that the corpus definition 
	can live anywhere in the file system
	'''
	testdir = tmpdir.mkdir('/testdir')
	copy(str(abspath('ianalyzer/corpora/times.py')), str(testdir))
	path_testfile = str(testdir)+'/times.py'
	monkeypatch.setattr(config, 'CORPORA', {'times': path_testfile})
	reload(corpora)
	assert corpora.corpus_obj
