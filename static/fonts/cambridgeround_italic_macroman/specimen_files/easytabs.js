/*
Case Conductor is a Test Case Management system.
Copyright (C) 2011 uTest Inc.

This file is part of Case Conductor.

Case Conductor is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Case Conductor is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.

*/
(function($){$.fn.easyTabs=function(option){var param=jQuery.extend({fadeSpeed:"fast",defaultContent:1,activeClass:'active'},option);$(this).each(function(){var thisId="#"+this.id;if(param.defaultContent==''){param.defaultContent=1;}
if(typeof param.defaultContent=="number")
{var defaultTab=$(thisId+" .tabs li:eq("+(param.defaultContent-1)+") a").attr('href').substr(1);}else{var defaultTab=param.defaultContent;}
$(thisId+" .tabs li a").each(function(){var tabToHide=$(this).attr('href').substr(1);$("#"+tabToHide).addClass('easytabs-tab-content');});hideAll();changeContent(defaultTab);function hideAll(){$(thisId+" .easytabs-tab-content").hide();}
function changeContent(tabId){hideAll();$(thisId+" .tabs li").removeClass(param.activeClass);$(thisId+" .tabs li a[href=#"+tabId+"]").closest('li').addClass(param.activeClass);if(param.fadeSpeed!="none")
{$(thisId+" #"+tabId).fadeIn(param.fadeSpeed);}else{$(thisId+" #"+tabId).show();}}
$(thisId+" .tabs li").click(function(){var tabId=$(this).find('a').attr('href').substr(1);changeContent(tabId);return false;});});}})(jQuery);