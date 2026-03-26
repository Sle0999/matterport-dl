import os
import tempfile
import unittest
from unittest import mock

import run


class RunPipBootstrapTests(unittest.TestCase):
    def test_uses_pip_executable_when_present(self):
        with tempfile.TemporaryDirectory() as td:
            bin_dir = os.path.join(td, "Scripts" if os.name == "nt" else "bin")
            os.makedirs(bin_dir, exist_ok=True)
            pip_path = os.path.join(bin_dir, "pip")
            with open(pip_path, "w", encoding="utf-8") as f:
                f.write("")

            cmd = run.get_pip_install_command(td)
            self.assertEqual(cmd, [pip_path])

    def test_bootstraps_when_pip_missing(self):
        with tempfile.TemporaryDirectory() as td:
            with mock.patch("run.subprocess.check_call") as check_call:
                cmd = run.get_pip_install_command(td)

            self.assertEqual(cmd, [run.sys.executable, "-m", "pip"])
            check_call.assert_any_call([run.sys.executable, "-m", "ensurepip", "--upgrade"])
            check_call.assert_any_call([run.sys.executable, "-m", "pip", "--version"])


if __name__ == "__main__":
    unittest.main()
