"""实际创建并移动 Windows 环境，验证旧目录消失后的自动适配。"""
import ensurepip
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[2]


class PythonEnvironmentTests(unittest.TestCase):
    def run_command(self, *args):
        result = subprocess.run([str(arg) for arg in args], capture_output=True,
                                encoding='utf-8', errors='replace', env={**os.environ, 'PYTHONUTF8': '1'})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_create_move_concurrent_repair_and_repeat(self):
        temporary_root = PROJECT / '.runtime-temp'
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root, prefix='python-relocation-') as folder:
            fixture = Path(folder).resolve()
            self.assertTrue(fixture.is_relative_to(temporary_root.resolve()))
            initial = fixture / 'before'
            (initial / 'scripts').mkdir(parents=True)
            for name in ('ensure_python.py', 'python-env.ps1', 'ensure-python.ps1'):
                shutil.copy2(PROJECT / 'scripts' / name, initial / 'scripts' / name)
            shutil.copytree(PROJECT / 'runtime' / 'python', initial / 'runtime' / 'python',
                            ignore=shutil.ignore_patterns('__pycache__', 'site-packages'))
            (initial / 'requirements.lock.txt').write_text(f'pip=={ensurepip.version()}\n', encoding='utf-8')
            self.run_command(initial / 'runtime/python/python.exe', '-I', '-X', 'utf8',
                             initial / 'scripts/ensure_python.py')
            self.assertTrue((initial / '.venv/Scripts/python.exe').is_file())
            moved = fixture / '复制后 项目'
            # 重命名整个测试目录；确认源和目标都在本次创建的测试范围内。
            self.assertEqual(initial.resolve().parent, fixture)
            self.assertEqual(moved.resolve().parent, fixture)
            initial.rename(moved)
            self.assertFalse(initial.exists())
            command = [str(moved / 'runtime/python/python.exe'), '-I', '-X', 'utf8',
                       str(moved / 'scripts/ensure_python.py')]
            processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                         for _ in range(2)]
            for process in processes:
                stdout, stderr = process.communicate(timeout=60)
                self.assertEqual(process.returncode, 0, (stdout + stderr).decode('utf-8', errors='replace'))
            info = json.loads(self.run_command(moved / '.venv/Scripts/python.exe', '-I', '-X', 'utf8', '-c',
                                              'import sys,json;print(json.dumps([sys.prefix,sys.base_prefix]))'))
            self.assertEqual(Path(info[0]), moved / '.venv')
            self.assertEqual(Path(info[1]), moved / 'runtime/python')
            pip_output = self.run_command(moved / '.venv/Scripts/pip.exe', '--version')
            self.assertIn(str(moved / '.venv'), pip_output)
            self.assertNotIn(str(initial), (moved / '.venv/pyvenv.cfg').read_text())
            activation = (moved / '.venv/Scripts/activate.bat').read_text()
            self.assertIn(str(moved / '.venv'), activation)
            self.assertNotIn(str(initial), activation)
            config_time = (moved / '.venv/pyvenv.cfg').stat().st_mtime_ns
            entry_time = (moved / '.venv/Scripts/pip.exe').stat().st_mtime_ns
            self.run_command(*command)
            self.assertEqual((moved / '.venv/pyvenv.cfg').stat().st_mtime_ns, config_time)
            self.assertEqual((moved / '.venv/Scripts/pip.exe').stat().st_mtime_ns, entry_time)
            self.run_command('powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                             moved / 'scripts/ensure-python.ps1')


if __name__ == '__main__':
    unittest.main()
