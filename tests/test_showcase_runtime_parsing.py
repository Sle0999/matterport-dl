import importlib.util
import pathlib
import sys
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "matterport-dl.py"
spec = importlib.util.spec_from_file_location("matterport_dl", MODULE_PATH)
matterport_dl = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = matterport_dl
spec.loader.exec_module(matterport_dl)


class ShowcaseRuntimeParsingTests(unittest.TestCase):
    def test_old_runtime_format(self):
        runtime = (
            'd.u=e=>"js/"+({239:"three-examples",777:"split"}[e]||e)+"."+{172:"6c50",9553:"8aa2"}[e]+".js",'
            'd.miniCssF=e=>"css/"+({7475:"late",9114:"core"}[e]||e)+"."+{7475:1,9114:1}[e]+".css"'
        )
        js_named, js_keys, css_named, css_keys = matterport_dl.parseShowcaseRuntimeDicts(runtime)

        self.assertEqual(js_named["239"], "three-examples")
        self.assertEqual(js_keys["172"], "6c50")
        self.assertEqual(css_named["7475"], "late")
        self.assertEqual(css_keys["9114"], "1")

    def test_new_runtime_format(self):
        runtime = (
            'd.u=e=>"js/"+({239:"three-examples",777:"split"}[e]||e)+"."+{172:"6c50",9553:"8aa2"}[e]+".js",'
            'd.miniCssF=e=>"css/"+({7475:"late",9114:"core"}[e]||e)+".css"'
        )
        js_named, js_keys, css_named, css_keys = matterport_dl.parseShowcaseRuntimeDicts(runtime)

        self.assertEqual(js_named["777"], "split")
        self.assertEqual(js_keys["9553"], "8aa2")
        self.assertEqual(css_named["9114"], "core")
        self.assertEqual(css_keys["7475"], "late")

    def test_ignores_other_js_strings_and_uses_u_mapping(self):
        runtime = (
            'x.s="js/browser-check.js",'
            'd.u=e=>"js/"+({7990:"init",1470:"vendors-common"}[e]||e)+"."+{7990:"abc123",1470:"def456"}[e]+".js",'
            'd.miniCssF=e=>"css/"+({7990:"init"}[e]||e)+".css",'
            'd.x=1'
        )
        js_named, js_keys, css_named, css_keys = matterport_dl.parseShowcaseRuntimeDicts(runtime)

        self.assertEqual(js_named["7990"], "init")
        self.assertEqual(js_keys["1470"], "def456")
        self.assertEqual(css_named["7990"], "init")
        self.assertEqual(css_keys["7990"], "init")

    def test_generates_plain_js_fallback_paths(self):
        runtime = 'd.e(7990),d.e(4892),d.e(1470)'
        js_named = {"7990": "init"}
        js_keys = {"1470": "def456"}

        fallback_files = matterport_dl.parseShowcaseRuntimeJSFallbackFiles(runtime, js_named, js_keys)

        self.assertIn("js/7990.js", fallback_files)
        self.assertIn("js/4892.js", fallback_files)
        self.assertIn("js/1470.js", fallback_files)
        self.assertIn("js/init.js", fallback_files)


if __name__ == "__main__":
    unittest.main()
