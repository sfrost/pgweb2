function display_default_font_size(id)
{
        var x = document.getElementById(id);

        if (x.currentStyle)
                var y = x.currentStyle['fontSize'];
        else if (window.getComputedStyle)
                var y = document.defaultView.getComputedStyle(x,null).getPropertyValue('font-size');
        return y;
}

document.write('<pre id="monotest" style="display: none;">&nbsp;</pre>');
document.write('<p id="paratest" style="display: none;">&nbsp;</p>');
var monoSize = parseInt(display_default_font_size("monotest"));
var propSize = parseInt(display_default_font_size("paratest"));
var newMonoSize = propSize / monoSize;

if (newMonoSize != 1)
{
        document.write('<style type="text/css" media="screen">'
					+ '#docContainer tt, #docContainer pre, #docContainer code'
					+ '{font-size: ' + newMonoSize.toFixed(1) + 'em;}\n'
					/* prevent embedded code tags from changing font size */
					+ '#docContainer code code'
					+ '{font-size: 1em;}</style>\n');
}

$('.navbar-lower').affix({
  offset: {top: 50}
});
