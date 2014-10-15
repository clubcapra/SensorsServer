<?php

class Sensor
{
	var $_numericID;
	var $_textID;
	var $_displayName;
	var $_img;
	
	function __construct($numericID, $textID, $displayName, $img)
	{
		$this->_numericID 	= $numericID;
		$this->_textID		= $textID;
		$this->_displayName	= $displayName;
		$this->_img			= $img;	
	}
	
	function getHTML()
	{
		$output = "";
		$output .= '<label>';
		$output .= '<div class="sensorBlock">';
		$output .= '<h1>'.$this->_displayName.'</h1>';
		$output .= '<img src="'.$this->_img.'" /> <br/>';
		$output .= '<input type="checkbox" id="'.$this->_textID.'" onclick="update(this, '.$this->_numericID.')" />';
		$output .= '</div>';
		$output .= '</label>';
		return $output;
	}
}

?>