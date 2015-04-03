import maltrieve
import requests


def test_basic_args():
    args = maltrieve.setup_args(['-l', 'testlog', '-p', '127.0.0.1:8080', '-d', '/opt/'])
    assert args.logfile == 'testlog'
    assert args.proxy == '127.0.0.1:8080'
    assert args.dumpdir == '/opt/'


def test_saving_args():
    args = maltrieve.setup_args(['-v', '-x', '-c', '-s'])
    assert args.viper
    assert args.vxcage
    assert args.cuckoo
    assert args.sort_mime


def test_read_alt_config():
    args = maltrieve.setup_args(['--config', 'maltrieve-test.cfg'])
    assert args.config == "maltrieve-test.cfg"


def test_config_args():
    args = maltrieve.setup_args(['-l', 'testlog', '-p', '127.0.0.1:8080', '-d', '/tmp/mwtest'])
    cfg = maltrieve.config(args, 'maltrieve-test.cfg')
    assert cfg.logfile == 'testlog'
    test_proxy = {'http': '127.0.0.1:8080'}
    assert cmp(cfg.proxy, test_proxy) == 0
    assert cfg.dumpdir == '/tmp/mwtest'


def test_alt_config():
    args = maltrieve.setup_args(['--config', 'maltrieve-test.cfg'])
    cfg = maltrieve.config(args, args.config)
    assert cfg.dumpdir == 'archive-test'
    assert cfg.logfile == 'maltrieve-test.log'
    test_ua = {'User-Agent': 'Test-Agent'}
    assert cmp(cfg.useragent, test_ua) == 0
    test_proxy = {'http': '127.0.0.1:3128'}
    assert cmp(cfg.proxy, test_proxy) == 0
    assert cfg.black_list == ['text/html', 'text/plain']
    assert cfg.white_list == ['application/pdf', 'application/x-dosexec']


def test_parse_simple_list():
    source = requests.get('http://xwell.org/assets/maltrieve-test.txt').text
    assert maltrieve.process_simple_list(source) == \
        set(['http://example.org/mylist', 'http://example.com/yourlist'])


def test_parse_xml_list():
    source = requests.get('http://xwell.org/assets/maltrieve-test-list.xml').text
    assert maltrieve.process_xml_list_title(source) == \
        set(['http://example.org/mylist', 'http://example.com/yourlist'])


def test_parse_xml_desc():
    source = requests.get('http://xwell.org/assets/maltrieve-test-desc.xml').text
    assert maltrieve.process_xml_list_desc(source) == \
        set(['http://example.org/mylist', 'http://example.com/yourlist'])


def test_load_hashes(hashfile='test-load-hashes.json'):
    assert maltrieve.load_hashes(hashfile) == \
        set(['d41d8cd98f00b204e9800998ecf8427e'])


def test_save_hashes():
    hashes = set(['d41d8cd98f00b204e9800998ecf8427e'])
    maltrieve.save_hashes(hashes, 'test-save-hashes.json')
    test_load_hashes('test-save-hashes.json')


def test_load_urls(urlfile='test-load-urls.json'):
    assert maltrieve.load_urls(urlfile) == \
        set(['http://example.com/badurl'])


def test_save_urls():
    urls = set(['http://example.com/badurl'])
    maltrieve.save_urls(urls, 'test-save-urls.json')
    test_load_urls('test-save-urls.json')
