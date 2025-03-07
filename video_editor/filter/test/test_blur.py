import unittest
import numpy as np
from filter.filters.blur import blur_apply


class TestBlurApply(unittest.TestCase):
    """
    Test for blur filter
    """

    def setUp(self):
        # create a dummy image (image of size 100x100 with 3 color channels)
        shape = (100, 100, 3)  # 100x100 image with 3 color channels
        # generate random integers between 0 and 255
        self.image = np.random.randint(0, 256, shape, dtype=np.uint8)

    def test_blur_apply_no_blur(self):
        # if value is 0, the function should return the same image
        result = blur_apply(self.image, 0)
        np.testing.assert_array_equal(result, self.image)

    def test_blur_apply_blurred(self):
        # if value > 0, the function should apply blur
        value = 3
        result = blur_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertFalse(
            np.array_equal(result, self.image)
        )  # check that the image changed

    def test_blur_apply_negative_value(self):
        # if value is negative, it should return the same image (assuming no exception handling)
        result = blur_apply(self.image, -1)
        np.testing.assert_array_equal(result, self.image)


if __name__ == "__main__":
    unittest.main()
