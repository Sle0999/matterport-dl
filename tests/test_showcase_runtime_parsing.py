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


if __name__ == "__main__":
    unittest.main()
