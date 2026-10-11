"""用当前项目的运行时修复复制后的虚拟环境，保留兼容的已安装依赖。"""
import hashlib
import importlib.metadata
import json
import msvcrt
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import venv

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / '.venv'
PYTHON = ENV / 'Scripts' / 'python.exe'
LOCK = ROOT / 'requirements.lock.txt'
MARKER = ENV / '.project-environment.json'


def run(*args):
    subprocess.run([str(arg) for arg in args], cwd=ROOT, check=True)


def missing_requirements():
    missing = []
    for line in LOCK.read_text(encoding='utf-8-sig').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        match = re.fullmatch(r'([\w.-]+)==([^\s;]+)', line)
        if match:
            name, version = match.groups()
        elif line.endswith('.whl'):
            name, version = Path(line).name.split('-')[:2]
        else:
            raise ValueError(f'不支持的依赖清单条目：{line}')
        try:
            installed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            installed = None
        if installed != version:
            missing.append(name)
    return missing


def refresh_launchers():
    # pip 的 Windows 命令入口也包含绝对路径；按照已安装包的入口元数据重新生成。
    from pip._vendor.distlib.scripts import ScriptMaker
    maker = ScriptMaker(None, str(ENV / 'Scripts'))
    maker.executable = str(PYTHON)
    maker.clobber = True
    maker.variants = {''}
    for distribution in importlib.metadata.distributions():
        for entry in distribution.entry_points:
            if entry.group in ('console_scripts', 'gui_scripts'):
                if Path(entry.name).name != entry.name or '/' in entry.name or '\\' in entry.name:
                    raise ValueError(f'无效命令入口：{entry.name}')
                maker.make(f'{entry.name} = {entry.value}', {'gui': entry.group == 'gui_scripts'})
    maker.make(f'pip{sys.version_info.major}.{sys.version_info.minor} = pip._internal.cli.main:main')


def prepare():
    expected = {
        'schema': 1,
        'root': str(ROOT),
        'runtime': str(Path(sys.executable).resolve()),
        'version': list(sys.version_info[:3]),
        'requirements': hashlib.sha256(LOCK.read_bytes()).hexdigest(),
    }
    try:
        marker = json.loads(MARKER.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        marker = None
    try:
        config = dict(line.split(' = ', 1) for line in (ENV / 'pyvenv.cfg').read_text().splitlines() if ' = ' in line)
    except OSError:
        config = {}
    correct_home = os.path.normcase(config.get('home', '')) == os.path.normcase(str(Path(sys.executable).parent))
    # 始终确认解释器与依赖可用；路径变化时不需要先启动旧虚拟环境。
    ready = False
    if correct_home and PYTHON.is_file():
        probe = subprocess.run([str(PYTHON), '-I', '-X', 'utf8', str(Path(__file__).resolve()), '--verify'],
                               cwd=ROOT, capture_output=True, text=True)
        ready = probe.returncode == 0
    if ready and marker == expected:
        return
    print('正在适配当前项目目录的 Python 环境……', flush=True)
    previous_version = config.get('version', '')
    if previous_version and previous_version.split('.')[:2] != [str(v) for v in sys.version_info[:2]]:
        raise RuntimeError('复制的环境与 runtime/python 的 Python 主次版本不同，请先备份并移走 .venv 后重试。')
    # clear=False 保留 site-packages；重新创建配置、解释器和激活脚本。
    venv.EnvBuilder(with_pip=False, clear=False, symlinks=False).create(ENV)
    pip_probe = subprocess.run([str(PYTHON), '-I', '-c', 'import pip'], cwd=ROOT, capture_output=True)
    if pip_probe.returncode:
        run(PYTHON, '-I', '-X', 'utf8', '-m', 'ensurepip', '--default-pip')
    probe = subprocess.run([str(PYTHON), '-I', '-X', 'utf8', str(Path(__file__).resolve()), '--verify'], cwd=ROOT)
    if probe.returncode:
        print('依赖缺失或版本不同，正在按 requirements.lock.txt 安装……', flush=True)
        run(PYTHON, '-I', '-X', 'utf8', '-m', 'pip', 'install', '-r', LOCK)
        run(PYTHON, '-I', '-X', 'utf8', Path(__file__).resolve(), '--verify')
    run(PYTHON, '-I', '-X', 'utf8', '-m', 'pip', 'check')
    run(PYTHON, '-I', '-X', 'utf8', Path(__file__).resolve(), '--refresh-launchers')
    temporary = MARKER.with_suffix('.tmp')
    temporary.write_text(json.dumps(expected, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(MARKER)
    print('Python 环境已适配当前目录。', flush=True)


def main():
    if sys.argv[1:] == ['--verify']:
        if Path(sys.prefix).resolve() != ENV or Path(sys.base_prefix).resolve() != ROOT / 'runtime' / 'python':
            return 1
        missing = missing_requirements()
        if missing:
            print('需要安装：' + ', '.join(missing), flush=True)
        return int(bool(missing))
    if sys.argv[1:] == ['--refresh-launchers']:
        refresh_launchers()
        return 0
    # 网页、worker、beat 同时启动时，避免它们同时改写虚拟环境。
    temporary_dir = ROOT / '.runtime-temp'
    temporary_dir.mkdir(exist_ok=True)
    os.environ['TMP'] = os.environ['TEMP'] = str(temporary_dir)
    tempfile.tempdir = str(temporary_dir)
    with (temporary_dir / 'python-environment.lock').open('a+b') as stream:
        if stream.tell() == 0:
            stream.write(b'0')
            stream.flush()
        deadline = time.monotonic() + 120
        while True:
            stream.seek(0)
            try:
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError('另一个启动入口正在准备 Python 环境，请稍后重试。')
                time.sleep(0.2)
        try:
            prepare()
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Python 环境准备失败：{error}', file=sys.stderr)
        sys.exit(1)
