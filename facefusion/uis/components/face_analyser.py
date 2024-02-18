from typing import Optional, Dict, Any, List

import gradio

import facefusion.globals
import facefusion.choices
from facefusion import wording
from facefusion.typing import FaceAnalyserOrder, FaceAnalyserAge, FaceAnalyserGender, FaceDetectorModel, FaceDetectorTweak
from facefusion.uis.core import register_ui_component

FACE_ANALYSER_ORDER_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_ANALYSER_AGE_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_ANALYSER_GENDER_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_DETECTOR_MODEL_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_DETECTOR_SIZE_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_DETECTOR_SCORE_SLIDER : Optional[gradio.Slider] = None
FACE_DETECTOR_TWEAKS_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None


def render() -> None:
	global FACE_ANALYSER_ORDER_DROPDOWN
	global FACE_ANALYSER_AGE_DROPDOWN
	global FACE_ANALYSER_GENDER_DROPDOWN
	global FACE_DETECTOR_MODEL_DROPDOWN
	global FACE_DETECTOR_SIZE_DROPDOWN
	global FACE_DETECTOR_SCORE_SLIDER
	global FACE_DETECTOR_TWEAKS_CHECKBOX_GROUP

	face_detector_size_dropdown_args : Dict[str, Any] =\
	{
		'label': wording.get('uis.face_detector_size_dropdown'),
		'value': facefusion.globals.face_detector_size
	}
	if facefusion.globals.face_detector_size in facefusion.choices.face_detector_set[facefusion.globals.face_detector_model]:
		face_detector_size_dropdown_args['choices'] = facefusion.choices.face_detector_set[facefusion.globals.face_detector_model]
	with gradio.Row():
		FACE_ANALYSER_ORDER_DROPDOWN = gradio.Dropdown(
			label = wording.get('uis.face_analyser_order_dropdown'),
			choices = facefusion.choices.face_analyser_orders,
			value = facefusion.globals.face_analyser_order
		)
		FACE_ANALYSER_AGE_DROPDOWN = gradio.Dropdown(
			label = wording.get('uis.face_analyser_age_dropdown'),
			choices = [ 'none' ] + facefusion.choices.face_analyser_ages,
			value = facefusion.globals.face_analyser_age or 'none'
		)
		FACE_ANALYSER_GENDER_DROPDOWN = gradio.Dropdown(
			label = wording.get('uis.face_analyser_gender_dropdown'),
			choices = [ 'none' ] + facefusion.choices.face_analyser_genders,
			value = facefusion.globals.face_analyser_gender or 'none'
		)
	FACE_DETECTOR_MODEL_DROPDOWN = gradio.Dropdown(
		label = wording.get('uis.face_detector_model_dropdown'),
		choices = facefusion.choices.face_detector_set.keys(),
		value = facefusion.globals.face_detector_model
	)
	FACE_DETECTOR_SIZE_DROPDOWN = gradio.Dropdown(**face_detector_size_dropdown_args)
	FACE_DETECTOR_SCORE_SLIDER = gradio.Slider(
		label = wording.get('uis.face_detector_score_slider'),
		value = facefusion.globals.face_detector_score,
		step = facefusion.choices.face_detector_score_range[1] - facefusion.choices.face_detector_score_range[0],
		minimum = facefusion.choices.face_detector_score_range[0],
		maximum = facefusion.choices.face_detector_score_range[-1]
	)
	FACE_DETECTOR_TWEAKS_CHECKBOX_GROUP = gradio.CheckboxGroup(
		label = wording.get('uis.face_detector_tweaks_checkbox_group'),
		value = facefusion.globals.face_detector_tweaks,
		choices = facefusion.choices.face_detector_tweaks
	)
	register_ui_component('face_analyser_order_dropdown', FACE_ANALYSER_ORDER_DROPDOWN)
	register_ui_component('face_analyser_age_dropdown', FACE_ANALYSER_AGE_DROPDOWN)
	register_ui_component('face_analyser_gender_dropdown', FACE_ANALYSER_GENDER_DROPDOWN)
	register_ui_component('face_detector_model_dropdown', FACE_DETECTOR_MODEL_DROPDOWN)
	register_ui_component('face_detector_size_dropdown', FACE_DETECTOR_SIZE_DROPDOWN)
	register_ui_component('face_detector_score_slider', FACE_DETECTOR_SCORE_SLIDER)
	register_ui_component('face_detector_tweaks_checkbox_group', FACE_DETECTOR_TWEAKS_CHECKBOX_GROUP)


def listen() -> None:
	FACE_ANALYSER_ORDER_DROPDOWN.change(update_face_analyser_order, inputs = FACE_ANALYSER_ORDER_DROPDOWN)
	FACE_ANALYSER_AGE_DROPDOWN.change(update_face_analyser_age, inputs = FACE_ANALYSER_AGE_DROPDOWN)
	FACE_ANALYSER_GENDER_DROPDOWN.change(update_face_analyser_gender, inputs = FACE_ANALYSER_GENDER_DROPDOWN)
	FACE_DETECTOR_MODEL_DROPDOWN.change(update_face_detector_model, inputs = FACE_DETECTOR_MODEL_DROPDOWN, outputs = FACE_DETECTOR_SIZE_DROPDOWN)
	FACE_DETECTOR_SIZE_DROPDOWN.change(update_face_detector_size, inputs = FACE_DETECTOR_SIZE_DROPDOWN)
	FACE_DETECTOR_SCORE_SLIDER.change(update_face_detector_score, inputs = FACE_DETECTOR_SCORE_SLIDER)
	FACE_DETECTOR_TWEAKS_CHECKBOX_GROUP.change(update_face_detector_tweaks, inputs = FACE_DETECTOR_TWEAKS_CHECKBOX_GROUP)


def update_face_analyser_order(face_analyser_order : FaceAnalyserOrder) -> None:
	facefusion.globals.face_analyser_order = face_analyser_order if face_analyser_order != 'none' else None


def update_face_analyser_age(face_analyser_age : FaceAnalyserAge) -> None:
	facefusion.globals.face_analyser_age = face_analyser_age if face_analyser_age != 'none' else None


def update_face_analyser_gender(face_analyser_gender : FaceAnalyserGender) -> None:
	facefusion.globals.face_analyser_gender = face_analyser_gender if face_analyser_gender != 'none' else None


def update_face_detector_model(face_detector_model : FaceDetectorModel) -> gradio.Dropdown:
	facefusion.globals.face_detector_model = face_detector_model
	if facefusion.globals.face_detector_size in facefusion.choices.face_detector_set[face_detector_model]:
		return gradio.Dropdown(value = '640x640', choices = facefusion.choices.face_detector_set[face_detector_model])
	return gradio.Dropdown(value = '640x640', choices = [ '640x640' ])


def update_face_detector_size(face_detector_size : str) -> None:
	facefusion.globals.face_detector_size = face_detector_size


def update_face_detector_score(face_detector_score : float) -> None:
	facefusion.globals.face_detector_score = face_detector_score


def update_face_detector_tweaks(face_detector_tweaks : List[FaceDetectorTweak]) -> None:
	facefusion.globals.face_detector_tweaks = face_detector_tweaks
