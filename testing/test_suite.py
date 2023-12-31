import os
import numpy as np
import time

from PIL import Image
from unittest import TestCase

from pipeline import *


class RegexTests(TestCase):

    def test_blank_regex(self):

        results = None
        actual = find_time_remaining_from_results(results)
        expected = None
        assert actual == expected, f"Expected {expected}, actual: {actual}."

        results = []
        actual = find_time_remaining_from_results(results)
        expected = None
        assert actual == expected, f"Expected {expected}, actual: {actual}."

    def test_regex_with_spaces(self):

        results = ["11:21 "]
        assert find_time_remaining_from_results(
            results) == "11:21", f"Expected 11:21, got: {find_time_remaining_from_results(results)}"

        results = ["A, 23237895", "3", "  0    8:   43   "]
        assert find_time_remaining_from_results(
            results) == "08:43", f"Expected 8:43, got: {find_time_remaining_from_results(results)}"

    def test_regex_no_match(self):

        results = ["Abc8:2as0r"]
        assert find_time_remaining_from_results(results) is None

        results = ["88:21"]
        assert find_time_remaining_from_results(results) is None

        results = ["0.21"]
        actual = find_time_remaining_from_results(results)
        expected = None
        assert actual == expected, f"Expected {expected}, actual: {actual}."

        results = ["31:21"]
        actual = find_time_remaining_from_results(results)
        expected = None
        assert actual == expected, f"Expected {expected}, actual: {actual}."

    def test_regex_edge_cases(self):

        results = ["20:00"]
        actual = find_time_remaining_from_results(results)
        expected = "20:00"
        assert actual == expected, f"Expected {expected}, actual: {actual}."

        results = ["080:23", "15:23.2", "2:30"]
        actual = find_time_remaining_from_results(results)
        expected = "15:23.2"
        assert actual == expected, f"Expected {expected}, actual: {actual}."


class TimeConversionTests(TestCase):

    def test_time_coversion_blank(self):

        time = None
        actual = convert_time_to_float(time)
        expected = None
        assert actual == expected, f"Expected {expected}, actual: {actual}."

        time = ""
        actual = convert_time_to_float(time)
        expected = None
        assert actual == expected, f"Expected {expected}, actual: {actual}."

    def test_time_coversion_standard(self):

        time = "1:23"
        actual = convert_time_to_float(time)
        expected = (60.0 * 1) + 23.0
        assert actual == expected, f"Expected {expected}, actual: {actual}."

        time = "08:45"
        actual = convert_time_to_float(time)
        expected = (60.0 * 8) + 45.0
        assert actual == expected, f"Expected {expected}, actual: {actual}."

        time = "50.2"
        actual = convert_time_to_float(time)
        expected = 50.2
        assert actual == expected, f"Expected {expected}, actual: {actual}."

    def test_time_rare_formatting(self):

        time = "09:45.2"
        actual = convert_time_to_float(time)
        expected = (60.0 * 9) + 45.0 + .2
        assert actual == expected, f"Expected {expected}, actual: {actual}."


class TextExtractionTests(TestCase):

    def test_blank_image(self):

        image = None
        actual = extract_text_with_paddle(image)
        expected = []
        assert actual == expected, f"Expected {expected}, actual: {actual}."

        image = None
        actual = extract_time_remaining_from_image(image)
        expected = None
        assert actual == expected, f"Expected {expected}, actual: {actual}."

    def test_no_time_remaining(self):

        image = Image.open(r"testing\assets\blank_images\black.png")
        actual = extract_time_remaining_from_image(image)
        expected = None
        assert actual == expected, f"Expected {expected}, actual: {actual}."

    def test_valid_time_remaining_(self):

        image = Image.fromarray(cv2.imread(
            r"testing\assets\example_cropped_rois\time_remaining\time_remaining_1.PNG"))
        actual = extract_time_remaining_from_image(image)
        expected = "2:41"
        assert actual == expected, f"Expected {expected}, actual: {actual}."


class TimeExtractionBenchmarkTests(TestCase):

    def test_100_whole_time_remaining_roi_benchmark(self):

        found, total = 0, 0
        dir = r"testing\assets\example_rois"
        rois = os.listdir(dir)
        roi_paths = [os.path.join(dir, roi) for roi in rois]
        for fp in roi_paths:
            img = Image.fromarray(cv2.imread(fp))
            result = extract_time_remaining_from_image(img)
            if result is not None:
                found += 1
            total += 1
        assert (found / total) >= .85

    def test_100_cropped_time_remaining_roi_benchmark(self):

        found, total = 0, 0
        dir = r"testing\assets\example_cropped_rois\time_remaining"
        rois = os.listdir(dir)
        roi_paths = [os.path.join(dir, roi) for roi in rois]
        for fp in roi_paths:
            img = Image.fromarray(cv2.imread(fp))
            result = extract_time_remaining_from_image(img)
            if result is not None:
                found += 1
            total += 1
        assert (found / total) >= .95
