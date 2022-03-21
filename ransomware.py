import os, sys, json, time, argparse, string, random, shutil, hashlib
from tkinter import *
from tkinter.ttk import *

from Crypto import Random
from Crypto.Cipher import AES


def parse_args():
    # Initialize parser
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')
    parser_list = sub_parsers.add_parser('list')
    #parser_list.add_argument('all', help='List ransomware patterns')

    parser_run = sub_parsers.add_parser('run')
    parser_run.add_argument(
        "-p",
        "--pattern",
        required=True,
        help="Audit event pattern"
    )
    parser_run.add_argument(
        "-d",
        "--dir",
        required=True,
        help="Input dir")
    parser_run.add_argument(
        "-e",
        "--extn",
        default="DATALENS",
        help="Blocked extension"
    )
    parser_run.add_argument(
        "-c",
        "--count",
        default=1,
        help="Total file count"
    )
    parser_run.add_argument(
        "-s",
        "--sleep",
        default=0,
        help="Sleep between tests"
    )
    parser_run.add_argument(
        "--encrypt",
        default=False,
        action="store_true",
        help="Encrypt file"
    )
    parser_run.add_argument(
        "--prefix",
        default=False,
        action="store_true",
        help="Add prefix to filename"
    )
    parser_run.add_argument(
        "--suffix",
        default=False,
        action="store_true",
        help="Add suffix to filename"
    )
    parser_run.add_argument(
        "--chdir",
        default=False,
        action="store_true",
        help="Change target dir"
    )
    parser_run.add_argument(
        "--loopback",
        default=False,
        action="store_true",
        help="Wait for loopback window completion"
    )
    args = parser.parse_args()

    return args


class EventManager(object):
    def __init__(self, args):
        self.args = args
        self.source = args.dir
        self.extn = args.extn
        self.count = int(args.count)
        self.sleep = int(args.sleep)
        self.encrypt = args.encrypt
        self.pattern = args.pattern
        self.loopback = args.loopback
        self.chdir = args.chdir
        self.prefix = None
        if args.prefix:
            self.prefix = self._gen_string(size=4)
        self.suffix = None
        if args.suffix:
            self.suffix = self._gen_string(size=4)
        self.target = self.source
        if args.chdir:
            self.target = self._create_data_dirs()
        self.result = list()
        self.key = self._hash_key()
        self._check_data_files()

    def _create_data_dirs(self):
        sub_dir = os.path.join(self.source, 'datalens')
        #top_dir = os.path.abspath(os.path.join(self.source, '..', 'datalens'))

        #for xdir in [sub_dir, top_dir]:
        for xdir in [sub_dir]:
            if not os.path.exists(xdir):
                os.makedirs(xdir)
        return xdir

    def _check_data_files(self):
        if not os.path.exists(self.source):
            self.result.append({'error': 'Input dir does not exist.'})
            sys.exit(2)

        file_exist_cnt = 0
        dir_list = os.listdir(self.source)
        for entry in dir_list:
            if entry.endswith('datalens.txt'):
                file_exist_cnt += 1

        if file_exist_cnt >= self.count:
            return True

        for i in range(self.count - file_exist_cnt):
            prefix = ''.join(
                random.choices(string.ascii_lowercase + string.digits, k=8)
            )
            txt_file = os.path.join(self.source, "{0}-datalens.txt".format(prefix))
            if not os.path.exists(txt_file):
                data = ''.join(
                    random.choices(string.ascii_uppercase + string.digits, k=1000)
                )

                file = open(txt_file, "w")
                file.write(data)
                file.close()

    def _hash_key(self):
        key = hashlib.md5(self._gen_string().encode("utf-8")).hexdigest()
        key = key.encode("utf-8")
        return key

    def _gen_string(
        self, size=64, chars=string.ascii_uppercase + string.digits
    ):
        return "".join(random.choice(chars) for _ in range(size))

    def _pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def _encrypt(self, message, key_size=256):
        if not self.encrypt:
            message += bytes(self._gen_string(), 'utf-8')
            return message

        message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def create_blocked_extn(self, source_file):
        name, extn = os.path.splitext(source_file)
        target_file = "{0}.{1}".format(name, self.extn)
        result = dict()
        result['action'] = 'copy'
        result['source'] = source_file
        result['target'] = target_file
        try:
            shutil.copy(source_file, target_file)
        except PermissionError as err:
            result['error'] = str(err)
        finally:
            self.result.append(result)

    def rename_blocked_extn(self, source_file):
        """
         - Extension (e.g. ppt) exists in the blocked list
         - rename file abc.txt to abc.ppt
        """
        name, extn = os.path.splitext(os.path.basename(source_file))
        if self.prefix:
            name = self.prefix + "_" + name
        if self.suffix:
            name = name + "_" + self.suffix

        target_file = os.path.join(
            self.target, "{0}.{1}".format(name, self.extn)
        )

        result = {
            'args': vars(self.args),
            'action': 'rename',
            'source': source_file,
            'target': target_file
        }
        try:
            os.rename(source_file, target_file)
        except Exception as err:
            result['error'] = str(err)
        finally:
            self.result.append(result)

    def write_rename_extn(self, source_file):
        name, extn = os.path.splitext(os.path.basename(source_file))
        if self.prefix:
            name = self.prefix + "_" + name
        if self.suffix:
            name = name + "_" + self.suffix

        target_file = os.path.join(
            self.target, "{0}.{1}".format(name, self.extn)
        )
        result = {}
        result['args'] = vars(self.args)
        result['source'] = source_file
        result['target'] = target_file
        result['action'] = 'rename'

        # read content andencrypt
        with open(source_file, "rb") as fo:
            plaintext = fo.read()

        # delayed encryption . uncomment sleep() for fast encryption
        # sleep(1)
        enc = self._encrypt(plaintext)

        # delayed encryption . uncomment sleep() for fast encryption
        # sleep(1)

        #  overwrite the file with encrypted data
        with open(source_file, "wb") as fo:
            fo.write(enc)

        if self.loopback:
            print("Sleep 15 mins until loopback window completion")
            time.sleep(900)
        # rename the file by changing the extension to DATALENS
        # delayed encryption . uncomment sleep() for fast encryption
        # sleep(1)
        try:
            os.rename(source_file, target_file)
        except Exception as err:
            result['error'] = str(err)
        finally:
            self.result.append(result)

    def write_remove_file(self, source_file):
        name, extn = os.path.splitext(os.path.basename(source_file))
        if self.prefix:
            name = self.prefix + "_" + name
        if self.suffix:
            name = name + "_" + self.suffix

        target_file = os.path.join(
            self.target, "{0}.{1}".format(name, self.extn)
        )

        result = {}
        result['args'] = vars(self.args)
        result['source'] = source_file
        result['target'] = target_file
        result['action'] = 'rename'

        # read content
        with open(source_file, "rb") as fo:
            plaintext = fo.read()
        # delayed encryption . uncomment sleep() for fast encryption
        # sleep(1)
        enc = self._encrypt(plaintext)
        # delayed encryption . uncomment sleep() for fast encryption
        # sleep(1)

        if self.loopback:
            print("Sleep 15 mins until loopback window completion")
            time.sleep(900)

        #  create an empty new file with filename.DATALENS
        # write encrypted content to the new file
        # delete the original file
        try:
            with open(target_file, "wb") as fo:
                fo.write(enc)
            os.remove(source_file)
        except Exception as err:
            result['error'] = str(err)
        finally:
            self.result.append(result)

    def run(self):
        if os.path.isdir(self.source):
            for path, subdirs, files in os.walk(self.source):
                for name in files:
                    if not name.endswith("datalens.txt"):
                        continue
                    source_file = os.path.join(path, name)
                    getattr(self, self.pattern)(source_file)
                    if self.sleep > 0:
                        time.sleep(self.sleep)
        else:
            getattr(self, self.pattern)(self.source)


class EventError(Exception):
    pass


def list_patterns():
    return [
        "rename_blocked_extn",
        "create_blocked_extn",
        "write_rename_extn",
        "write_remove_file"
    ]


def main():
    args = parse_args()
    patterns = list_patterns()

    if args.command == 'list':
        print("Possible event patterns :-")
        for count, entry in enumerate(patterns):
            print("  {0}. {1}".format(count + 1, entry))
        sys.exit(0)
    elif args.command == 'run':
        args.pattern = patterns[int(args.pattern) - 1]

    event = EventManager(args)
    try:
        event.run()
    finally:
        print(json.dumps(event.result, indent=4))


if __name__ == "__main__":
    main()
