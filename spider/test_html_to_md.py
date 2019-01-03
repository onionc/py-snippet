# coding:utf-8
""" 分析博客文章 """

import bs4
from bs4 import BeautifulSoup
import logging
import re
logging.basicConfig(level=logging.DEBUG)


def html_to_md(content_tag):
    """ 文章内容html解析为md """
    _code_class = 'crayon-row'

    if not isinstance(content_tag, bs4.element.Tag):
        raise TypeError("content_tag must be bs4.element.Tag type.")
    # 防止取到此节点之后，将此文档树独立出来使用
    content_tag = content_tag.extract()
    content_text = []
    tag = content_tag
    
    # for tag in content_tag.next_elements:
    while True:
        try:
            tag_name = tag.name
            logging.info(f"content:{tag}  tag:{tag_name}")

            if tag_name == 'a':
                # 链接
                logging.debug("链接")
                href = tag.get('href', '')
                title = tag.string

                # to md
                md_img = f"[{title}]({href})"
                content_text.append(md_img)

                tag = tag.parent.next_sibling

            elif tag_name == 'img':
                # 图片
                logging.debug("图片")
                src = tag.get('src', '')

                # to md
                md_img = f"![]({src})"
                content_text.append(md_img)

            elif tag_name == 'tr' and tag.has_attr('class') and _code_class in tag['class']:
                logging.debug("代码块")
                # 获取每行code，添加回车
                temp_code = []
                for line in tag.select('div.crayon-line')[:]:
                    line_code = line.get_text()
                    if line_code == '\xa0':
                        continue
                    temp_code.append(line_code)
                code = '\n'.join(temp_code)
                logging.debug(f"code={code}")

                # to md
                md_code = f"""
```
{code}
```
"""
                content_text.append(md_code)

                # 避免内容再取到，取前一个对象的兄弟标签，continue的接管必须有标签节点的变更，不然死循环
                # tag = tag.previous_element.previous_element.next_sibling
                tag = tag.parent.parent.next_sibling

            elif tag_name is None:
                # 文本内容
                logging.debug(f"other: {tag.string}")

                if isinstance(tag, bs4.element.Comment):
                    # 注释
                    pass
                elif tag.string == '\n':
                    pass
                else:
                    # 追加普通内容
                    content_text.append(tag.string)
                    pass
            elif re.search(r'h\d', tag_name):
                logging.debug("标题")
                head_grade = int(re.sub(r"h(\d)", r"\1",tag_name))
                md_head = f"{'#'*head_grade} {tag.string}"
                content_text.append(md_head)
                tag = tag.next_element

            # 下一个标签
            tag = tag.next_element
        except AttributeError as e:
            print("AttributeError:", e)
            break
        except Exception as e:
            print("Exception:", e)
            break

    return content_text

# url = http://www.alloyteam.com/2018/04/gka-ratio/
data="""

<!DOCTYPE html>
<html lang="zh-CN" xmlns:wb="http://open.weibo.com/wb">
<head>
<meta charset="UTF-8" />
<meta property="qc:admins" content="147062105661447145156375" />
<title>快速制作多倍图帧动画方式及原理:gka[&#8211;ratio] | AlloyTeam</title>
<link rel="profile" href="http://gmpg.org/xfn/11" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.alloyteam.com/wp-content/themes/alloyteam/style.css" />
<link rel="pingback" href="" />
<!--[if lt IE 9]>
<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
<link rel='dns-prefetch' href='//s.w.org' />
<link rel="alternate" type="application/rss+xml" title="AlloyTeam &raquo; 快速制作多倍图帧动画方式及原理:gka[&#8211;ratio]评论Feed" href="http://www.alloyteam.com/2018/04/gka-ratio/feed/" />
		<script type="text/javascript">
			window._wpemojiSettings = {"baseUrl":"https:\/\/s.w.org\/images\/core\/emoji\/2.2.1\/72x72\/","ext":".png","svgUrl":"https:\/\/s.w.org\/images\/core\/emoji\/2.2.1\/svg\/","svgExt":".svg","source":{"concatemoji":"http:\/\/www.alloyteam.com\/wp-includes\/js\/wp-emoji-release.min.js?ver=4.7.2"}};
			!function(a,b,c){function d(a){var b,c,d,e,f=String.fromCharCode;if(!k||!k.fillText)return!1;switch(k.clearRect(0,0,j.width,j.height),k.textBaseline="top",k.font="600 32px Arial",a){case"flag":return k.fillText(f(55356,56826,55356,56819),0,0),!(j.toDataURL().length<3e3)&&(k.clearRect(0,0,j.width,j.height),k.fillText(f(55356,57331,65039,8205,55356,57096),0,0),b=j.toDataURL(),k.clearRect(0,0,j.width,j.height),k.fillText(f(55356,57331,55356,57096),0,0),c=j.toDataURL(),b!==c);case"emoji4":return k.fillText(f(55357,56425,55356,57341,8205,55357,56507),0,0),d=j.toDataURL(),k.clearRect(0,0,j.width,j.height),k.fillText(f(55357,56425,55356,57341,55357,56507),0,0),e=j.toDataURL(),d!==e}return!1}function e(a){var c=b.createElement("script");c.src=a,c.defer=c.type="text/javascript",b.getElementsByTagName("head")[0].appendChild(c)}var f,g,h,i,j=b.createElement("canvas"),k=j.getContext&&j.getContext("2d");for(i=Array("flag","emoji4"),c.supports={everything:!0,everythingExceptFlag:!0},h=0;h<i.length;h++)c.supports[i[h]]=d(i[h]),c.supports.everything=c.supports.everything&&c.supports[i[h]],"flag"!==i[h]&&(c.supports.everythingExceptFlag=c.supports.everythingExceptFlag&&c.supports[i[h]]);c.supports.everythingExceptFlag=c.supports.everythingExceptFlag&&!c.supports.flag,c.DOMReady=!1,c.readyCallback=function(){c.DOMReady=!0},c.supports.everything||(g=function(){c.readyCallback()},b.addEventListener?(b.addEventListener("DOMContentLoaded",g,!1),a.addEventListener("load",g,!1)):(a.attachEvent("onload",g),b.attachEvent("onreadystatechange",function(){"complete"===b.readyState&&c.readyCallback()})),f=c.source||{},f.concatemoji?e(f.concatemoji):f.wpemoji&&f.twemoji&&(e(f.twemoji),e(f.wpemoji)))}(window,document,window._wpemojiSettings);
		</script>
		<style type="text/css">
img.wp-smiley,
img.emoji {
	display: inline !important;
	border: none !important;
	box-shadow: none !important;
	height: 1em !important;
	width: 1em !important;
	margin: 0 .07em !important;
	vertical-align: -0.1em !important;
	background: none !important;
	padding: 0 !important;
}
</style>
<link rel='stylesheet' id='crayon-css'  href='http://www.alloyteam.com/wp-content/plugins/crayon-syntax-highlighter/css/min/crayon.min.css?ver=_2.7.2_beta' type='text/css' media='all' />
<link rel='stylesheet' id='crayon-theme-sublime-text-css'  href='http://www.alloyteam.com/wp-content/plugins/crayon-syntax-highlighter/themes/sublime-text/sublime-text.css?ver=_2.7.2_beta' type='text/css' media='all' />
<link rel='stylesheet' id='crayon-font-courier-new-css'  href='http://www.alloyteam.com/wp-content/plugins/crayon-syntax-highlighter/fonts/courier-new.css?ver=_2.7.2_beta' type='text/css' media='all' />
<link rel='stylesheet' id='wsw-font-awesome-css-css'  href='http://www.alloyteam.com/wp-content/plugins/seo-wizard/css/font-awesome-4.2.0/css/font-awesome.min.css?ver=1.0.0' type='text/css' media='all' />
<script type='text/javascript' src='http://www.alloyteam.com/wp-includes/js/jquery/jquery.js?ver=1.12.4'></script>
<script type='text/javascript' src='http://www.alloyteam.com/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1'></script>
<script type='text/javascript'>
/* <![CDATA[ */
var CrayonSyntaxSettings = {"version":"_2.7.2_beta","is_admin":"0","ajaxurl":"http:\/\/www.alloyteam.com\/wp-admin\/admin-ajax.php","prefix":"crayon-","setting":"crayon-setting","selected":"crayon-setting-selected","changed":"crayon-setting-changed","special":"crayon-setting-special","orig_value":"data-orig-value","debug":""};
print(line,type(line))var CrayonSyntaxStrings = {"copy":"\u4f7f\u7528 %s \u590d\u5236\uff0c\u4f7f\u7528 %s \u7c98\u8d34\u3002","minimize":"\u70b9\u51fb\u5c55\u5f00\u4ee3\
#u7801"};
/* ]]> */
</script>
<script type='text/javascript' src='http://www.alloyteam.com/wp-content/plugins/crayon-syntax-highlighter/js/min/crayon.min.js?ver=_2.7.2_beta'></script>
<link rel='https://api.w.org/' href='http://www.alloyteam.com/wp-json/' />
<link rel='prev' title='要做软件工程师，而不是前端工程师' href='http://www.alloyteam.com/2018/03/13344/' />
<link rel='next' title='多个动画间存在部分相同动画的优化方案:gka' href='http://www.alloyteam.com/2018/04/gka-optimize/' />
<meta name="generator" content="WordPress 4.7.2" />
<link rel="canonical" href="http://www.alloyteam.com/2018/04/gka-ratio/" />
<link rel='shortlink' href='http://www.alloyteam.com/?p=13371' />
<link rel="alternate" type="application/json+oembed" href="http://www.alloyteam.com/wp-json/oembed/1.0/embed?url=http%3A%2F%2Fwww.alloyteam.com%2F2018%2F04%2Fgka-ratio%2F" />
<link rel="alternate" type="text/xml+oembed" href="http://www.alloyteam.com/wp-json/oembed/1.0/embed?url=http%3A%2F%2Fwww.alloyteam.com%2F2018%2F04%2Fgka-ratio%2F&#038;format=xml" />

<!-- prettyPhoto 3.1.6 / gallery 1.0 -->
<link rel="stylesheet" href="http://www.alloyteam.com/wp-content/plugins/images-lazyload-and-slideshow/effects/prettyPhoto 3.1.6/css/prettyPhoto.css" type="text/css" media="screen"/>
<script type="text/javascript" src="http://www.alloyteam.com/wp-content/plugins/images-lazyload-and-slideshow/effects/prettyPhoto 3.1.6/js/jquery.prettyPhoto.js"></script>
<script type="text/javascript">
jQuery(function($){
	$(".content_banner img").each(function(i){
		_self = $(this);

		selfWidth = _self.attr("width")?_self.attr("width"):_self.width();
		selfHeight = _self.attr("height")?_self.attr("height"):_self.height();
		if ((selfWidth && selfWidth<50)
				|| (selfHeight && selfHeight<50)) {
			return;
		}

		if (this.parentNode.href) {
			aHref = this.parentNode.href;
			var b=/.+(\.jpg)|(\.jpeg)|(\.png)|(\.gif)|(\.bmp)/i;
			if (! b.test(aHref)) {
				return;
			}

			_self.addClass("ls_slideshow_imgs");

			_parentA = $(this.parentNode);
			rel = _parentA.attr("rel");
			if (! rel) {
				rel = "";
			}
			if (rel.indexOf("prettyPhoto") != 0) {
				_parentA.attr("rel","prettyPhoto[1]");
			}
		} else {
			imgsrc = "";
			if (_self.attr("src")) {
				imgsrc = _self.attr("src");
			}
			if (_self.attr("file")) {
				imgsrc = _self.attr("file");
			} else if (_self.attr("original")) {
				imgsrc = _self.attr("original");
			}

			if (imgsrc) {
				_self.addClass("ls_slideshow_imgs");
				_self.wrap("<a href='"+imgsrc+"' rel='prettyPhoto[1]'></a>");
			}
		}
	});

	$("a[rel^='prettyPhoto']").prettyPhoto({social_tools:""});
});
</script>
<!-- prettyPhoto 3.1.6 / gallery 1.0 end -->
<!------------ Created by Seo Wizard Wordpress Plugin - www.seo.uk.net -----------><meta name="robots" content="index,follow" />
<!------------------------------------------------------------------------------>		<style type="text/css">.recentcomments a{display:inline !important;padding:0 !important;margin:0 !important;}</style>
		<style type="text/css" media="screen">body{position:relative}#dynamic-to-top{display:none;overflow:hidden;width:auto;z-index:90;position:fixed;bottom:20px;right:20px;top:auto;left:auto;font-family:sans-serif;font-size:1em;color:#fff;text-decoration:none;text-shadow:0 1px 0 #333;font-weight:bold;padding:20px 23px;border:0px solid #aba6a6;background:#A9D5F4;-webkit-background-origin:border;-moz-background-origin:border;-icab-background-origin:border;-khtml-background-origin:border;-o-background-origin:border;background-origin:border;-webkit-background-clip:padding-box;-moz-background-clip:padding-box;-icab-background-clip:padding-box;-khtml-background-clip:padding-box;-o-background-clip:padding-box;background-clip:padding-box;-webkit-box-shadow:inset 0 0 0 1px rgba( 0, 0, 0, 0.2 ), inset 0 1px 0 rgba( 255, 255, 255, .4 ), inset 0 10px 10px rgba( 255, 255, 255, .1 );-ms-box-shadow:inset 0 0 0 1px rgba( 0, 0, 0, 0.2 ), inset 0 1px 0 rgba( 255, 255, 255, .4 ), inset 0 10px 10px rgba( 255, 255, 255, .1 );-moz-box-shadow:inset 0 0 0 1px rgba( 0, 0, 0, 0.2 ), inset 0 1px 0 rgba( 255, 255, 255, .4 ), inset 0 10px 10px rgba( 255, 255, 255, .1 );-o-box-shadow:inset 0 0 0 1px rgba( 0, 0, 0, 0.2 ), inset 0 1px 0 rgba( 255, 255, 255, .4 ), inset 0 10px 10px rgba( 255, 255, 255, .1 );-khtml-box-shadow:inset 0 0 0 1px rgba( 0, 0, 0, 0.2 ), inset 0 1px 0 rgba( 255, 255, 255, .4 ), inset 0 10px 10px rgba( 255, 255, 255, .1 );-icab-box-shadow:inset 0 0 0 1px rgba( 0, 0, 0, 0.2 ), inset 0 1px 0 rgba( 255, 255, 255, .4 ), inset 0 10px 10px rgba( 255, 255, 255, .1 );box-shadow:inset 0 0 0 1px rgba( 0, 0, 0, 0.2 ), inset 0 1px 0 rgba( 255, 255, 255, .4 ), inset 0 10px 10px rgba( 255, 255, 255, .1 );-webkit-border-radius:0px;-moz-border-radius:0px;-icab-border-radius:0px;-khtml-border-radius:0px;border-radius:0px}#dynamic-to-top:hover{background:#54ba8f;background:#A9D5F4 -webkit-gradient( linear, 0% 0%, 0% 100%, from( rgba( 255, 255, 255, .2 ) ), to( rgba( 0, 0, 0, 0 ) ) );background:#A9D5F4 -webkit-linear-gradient( top, rgba( 255, 255, 255, .2 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -khtml-linear-gradient( top, rgba( 255, 255, 255, .2 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -moz-linear-gradient( top, rgba( 255, 255, 255, .2 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -o-linear-gradient( top, rgba( 255, 255, 255, .2 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -ms-linear-gradient( top, rgba( 255, 255, 255, .2 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -icab-linear-gradient( top, rgba( 255, 255, 255, .2 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 linear-gradient( top, rgba( 255, 255, 255, .2 ), rgba( 0, 0, 0, 0 ) );cursor:pointer}#dynamic-to-top:active{background:#A9D5F4;background:#A9D5F4 -webkit-gradient( linear, 0% 0%, 0% 100%, from( rgba( 0, 0, 0, .3 ) ), to( rgba( 0, 0, 0, 0 ) ) );background:#A9D5F4 -webkit-linear-gradient( top, rgba( 0, 0, 0, .1 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -moz-linear-gradient( top, rgba( 0, 0, 0, .1 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -khtml-linear-gradient( top, rgba( 0, 0, 0, .1 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -o-linear-gradient( top, rgba( 0, 0, 0, .1 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -ms-linear-gradient( top, rgba( 0, 0, 0, .1 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 -icab-linear-gradient( top, rgba( 0, 0, 0, .1 ), rgba( 0, 0, 0, 0 ) );background:#A9D5F4 linear-gradient( top, rgba( 0, 0, 0, .1 ), rgba( 0, 0, 0, 0 ) )}#dynamic-to-top,#dynamic-to-top:active,#dynamic-to-top:focus,#dynamic-to-top:hover{outline:none}#dynamic-to-top span{display:block;overflow:hidden;width:14px;height:12px;background:url( http://www.alloyteam.com/wp-content/plugins/dynamic-to-top/css/images/up.png )no-repeat center center}</style>		<style type="text/css" id="wp-custom-css">
			/*
您可以在此处加入您的CSS。

点击上方的帮助图标来了解更多。
*/
.entry-media {
	display: none;
}
body {
	-webkit-overflow-scrolling: touch;
}
.top-admin {
	display: none;
}
.related-post {
	margin-top: 0;
    margin-bottom: 40px;
}
h1 {
	font-size: 26px;
}
h2 {
	font-size: 16px;
}
.entry-title {
	line-height: 1.3;
	font-weight: bold;
	white-space: normal;
}
.entry-content h3::before {
	content: "";
    margin-left: 0;
}
.entry-content h3::after {
    content: "";
    margin-left: 0;
}
.posts-navigation {
	margin-top: -22px;
}
.site-footer {
    margin-top: 30px;
	border: 0;
}
.col-xs-6 {
    width: 100%;
}
.related-post {
    margin-bottom: 10px;
}
#ds-thread {
	margin-top: 45px;
    border-top: 1px solid rgba(0,0,0,0.13);
}
#ds-thread #ds-reset .ds-meta {
	border-bottom: 0;
}
.hentry {
	margin-bottom: 22px;
}
.related-posts-border {
	box-shadow: none;
}
/* 二维码占坑 */
.mobile-qrcode-wrapper {
	display: none;
}
/* 作者信息占坑 */
.mobile-author-info-wrapper {
	display:block;
}
.mobile-author-name-wrapper {
	margin-bottom: 18px;
}
.single .site-header .site-branding {
	display: none;
}
.single .site-header {
	margin: 0;
}
.single .container {
	padding-top: 44px;
}
.single .top-bar .container {
	padding-top: 0;
}
/* 头像部分 */
.mobile-author-img-wrapper {
	display: inline-block;
    width: 30px;
    height: 30px;
    vertical-align: 4px;
}
.mobile-author-name-wrapper {
	display: inline-block;
}
.mobile-body small {
	display: none;
}
.crayon-main {
	overflow-y: hidden;
}

/** PC **/
.c_time {
	font-size:14px;
}		</style>
	

<script type="text/JavaScript">
function addCookie(){　 // 加入收藏夹
	if (document.all){
		window.external.addFavorite('http://www.alloyteam.com', 'AlloyTeam - 腾讯全端 AlloyTeam 团队 Blog');
	}else if (window.sidebar){
		window.sidebar.addPanel('AlloyTeam - 腾讯全端 AlloyTeam 团队 Blog', 'http://www.alloyteam.com', "");
	}
}
</script>
<script src="http://tjs.sjs.sinajs.cn/open/api/js/wb.js" type="text/javascript" charset="utf-8"></script>
</head>

<body class="home blog" style="display:none;">
<!--[if IE]> 
<script>document.body.style.display = "block";</script>
<![endif]-->  
<!-- 注释 -->
<div id="alloy">
	<h1 id ="alloyteam" class="alloyteam1">AlloyTeam</h1>
	<h1 id ="alloyteam2" class="alloyteam2"><a href="/">AlloyTeam</a></h1>
	<div id ="tencentInfo">Copyright &copy; <script>document.write(new Date().getFullYear());</script> Tencent AlloyTeam. All Rights Reserved.</div>

</div>

<!--Header-->
<div id="header">
	<div id="top">
		<div id="nav">
			<a onfocus="this.blur()" href="http://www.alloyteam.com" id="logo" title="腾讯全端 AlloyTeam 团队 Blog"><cite>AlloyTeam</cite></a>
			<span class="subtitle">腾讯全端 AlloyTeam 团队 Blog</span>
			<div id="menu">
				<div class="widget_search">
					<form method="get" id="searchform" action="http://www.alloyteam.com/index.php" target="_blank">
						<input name="s" type="text" value="Search" onfocus="this.value='';" onblur="if(this.value==''){this.value='Search';}">
						<input name="" type="submit" value="" class="so" onmouseout="this.className='so'" onmouseover="this.className='soHover'">
					</form>
				</div>
			</div>
		</div>
	</div>
</div>
<div class="clearfix"></div>	
<div id="main">
	<div id="access">
	<div class="menu-navmenu-container"><ul id="menu-navmenu" class="menu"><li id="menu-item-29" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-29"><a title="腾讯Web前端团队博客 AlloyTeam 首页" href="http://www.alloyteam.com/page/0/">首页</a></li>
<li id="menu-item-740" class="menu-item menu-item-type-taxonomy menu-item-object-category current-post-ancestor current-menu-parent current-post-parent menu-item-has-children menu-item-740"><a href="http://www.alloyteam.com/webdevelop/">Web开发</a>
<ul class="sub-menu">
	<li id="menu-item-745" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-745"><a href="http://www.alloyteam.com/webdevelop/web-%e5%89%8d%e7%ab%af%e8%b5%84%e8%ae%af/">前端资讯</a></li>
	<li id="menu-item-855" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-855"><a href="http://www.alloyteam.com/webdevelop/html5/">HTML5</a></li>
	<li id="menu-item-856" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-856"><a href="http://www.alloyteam.com/webdevelop/css3/">CSS3</a></li>
	<li id="menu-item-854" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-854"><a href="http://www.alloyteam.com/webdevelop/javascript/">JavaScript</a></li>
	<li id="menu-item-5200" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-5200"><a href="http://www.alloyteam.com/webdevelop/node/">Node.js</a></li>
	<li id="menu-item-5201" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-5201"><a href="http://www.alloyteam.com/mobiledevelop/mobileweb/">移动 Web 开发</a></li>
	<li id="menu-item-747" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-747"><a href="http://www.alloyteam.com/webdevelop/ued/">用户体验设计</a></li>
	<li id="menu-item-857" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-857"><a href="http://www.alloyteam.com/webdevelop/web-%e5%89%8d%e7%ab%af%e4%bc%98%e5%8c%96/">Web 前端优化</a></li>
</ul>
</li>
<li id="menu-item-5194" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-has-children menu-item-5194"><a href="http://www.alloyteam.com/mobiledevelop/">移动开发</a>
<ul class="sub-menu">
	<li id="menu-item-5195" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-5195"><a href="http://www.alloyteam.com/mobiledevelop/android/">Android 开发</a></li>
	<li id="menu-item-5198" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-5198"><a href="http://www.alloyteam.com/mobiledevelop/ios-develop/">iOS 开发</a></li>
	<li id="menu-item-5199" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-5199"><a href="http://www.alloyteam.com/mobiledevelop/mobileweb/">移动 Web 开发</a></li>
</ul>
</li>
<li id="menu-item-748" class="menu-item menu-item-type-taxonomy menu-item-object-category current-post-ancestor current-menu-parent current-post-parent menu-item-748"><a href="http://www.alloyteam.com/%e8%b5%84%e6%ba%90%e5%b7%a5%e5%85%b7/">资源工具</a></li>
<li id="menu-item-1371" class="menu-item menu-item-type-taxonomy menu-item-object-category current-post-ancestor current-menu-parent current-post-parent menu-item-has-children menu-item-1371"><a href="http://www.alloyteam.com/alloylabs/">Alloy实验室</a>
<ul class="sub-menu">
	<li id="menu-item-744" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-744"><a href="http://www.alloyteam.com/alloylabs/showcase/">作品</a></li>
	<li id="menu-item-961" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-961"><a href="http://www.alloyteam.com/alloylabs/html5game/">HTML5游戏</a></li>
</ul>
</li>
<li id="menu-item-853" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-853"><a title="我们在 Github.com 上的 Web 开源项目" href="http://AlloyTeam.github.com">Github</a></li>
<li id="menu-item-746" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-746"><a href="http://www.alloyteam.com/team/">团队</a></li>
<li id="menu-item-1327" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-1327"><a href="http://www.alloyteam.com/message-board/">留言</a>
<ul class="sub-menu">
	<li id="menu-item-1335" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1335"><a href="http://www.alloyteam.com/links/">友情链接</a></li>
</ul>
</li>
<li id="menu-item-27" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-27"><a title="腾讯AlloyTeam" href="http://www.alloyteam.com/about/">关于</a></li>
<li id="menu-item-6875" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-6875"><a href="http://www.alloyteam.com/feed/">RSS</a></li>
</ul></div>	</div>

<!--Header End-->
<div id="content" role="main">	
    <div id="postlist">
    	        <div class="content_text"> 

        <div class="title1"> 
        <a href="http://www.alloyteam.com/author/tat-joeyguo/" class="test1 animated tada singleauthor" target="_blank"><img alt='TAT.joeyguo' src='http://www.alloyteam.com/wp-content/uploads/2015/12/TAT.joey_avatar_1451283400-43x43.jpg' class='avatar avatar-43 photo' height='43' width='43' /></a> 
       
        <a href="http://www.alloyteam.com/2018/04/gka-ratio/" class="blogTitle btitle" rel="bookmark" title="快速制作多倍图帧动画方式及原理:gka[&#8211;ratio]">快速制作多倍图帧动画方式及原理:gka[&#8211;ratio]</a> 
        <div class="blogPs"> In <a href="http://www.alloyteam.com/alloylabs/" rel="category tag">Alloy 实验室</a>,<a href="http://www.alloyteam.com/webdevelop/" rel="category tag">Web开发</a>,<a href="http://www.alloyteam.com/%e8%b5%84%e6%ba%90%e5%b7%a5%e5%85%b7/" rel="category tag">资源工具</a> on 2018年04月25日 by <a href="http://www.alloyteam.com/author/tat-joeyguo/" title="由TAT.joeyguo发布" rel="author">TAT.joeyguo</a>  view: 976 </div> 
        <span class="comments"><a href="http://www.alloyteam.com/2018/04/gka-ratio/#respond" class="up" >0</a></span>
        </div> 
        <!--content_banner_single--> 
        <div class="content_banner"> 
        

    	
        <div class="text">
        <p><a rel="nofollow" href="https://github.com/gkajs/gka/wiki/%E5%BF%AB%E9%80%9F%E5%88%B6%E4%BD%9C%E5%A4%9A%E5%80%8D%E5%9B%BE%E5%B8%A7%E5%8A%A8%E7%94%BB%E6%96%B9%E5%BC%8F%E5%8F%8A%E5%8E%9F%E7%90%86:gka%5B--ratio%5D">原文地址</a></p>
<p><img title="" src="https://user-images.githubusercontent.com/10385585/28303811-86f0aad0-6bc7-11e7-82da-8ee3a412eb43.jpg" alt="gka" /></p>
<p>多倍图的适配在前端开发还是比较常见的，像在 Retina 屏幕，一般会使用二倍图从而让图片保持清晰，而在开发帧动画中使用的图片实际上同样需要做这样的适配处理。gka提供一键式的制作多倍图帧动画的方式。</p>
<p><a rel="nofollow" href="https://github.com/joeyguo/gka">gka</a> 是一款简单的、高效的帧动画生成工具，图片处理工具。</p>
<p>官方文档：<a rel="nofollow" href="https://gka.js.org">https://gka.js.org</a></p>
<p>Github：<a rel="nofollow" href="https://github.com/gkajs/gka">https://github.com/gkajs/gka</a></p>
<p><span id="more-13371"></span></p>
<h1>使用gka生成多倍图帧动画的方式</h1>
<h2>方式一：对单一文件夹图片进行处理</h2>
<p>举例，2倍图的图片文件夹地址为 /workspace/img/</p>
<table>
<thead>
<tr>
<th>文件夹：/workspace/img/</th>
</tr>
</thead>
<tbody>
<tr>
<td><!-- Crayon Syntax Highlighter v_2.7.2_beta -->

		<div id="crayon-5c2da9c3bf5ac440116535" class="crayon-syntax crayon-theme-sublime-text crayon-font-courier-new crayon-os-pc print-yes notranslate" data-settings=" minimize scroll-mouseover" style=" margin-top: 1px; margin-bottom: 1px; font-size: 14px !important; line-height: 15px !important;">
		
			<div class="crayon-plain-wrap"></div>
			<div class="crayon-main" style="">
				<table class="crayon-table">
					<tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 14px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5c2da9c3bf5ac440116535-1">1</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5ac440116535-2">2</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5ac440116535-3">3</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5ac440116535-4">4</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5ac440116535-5">5</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5ac440116535-6">6</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5ac440116535-7">7</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 14px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5c2da9c3bf5ac440116535-1">&nbsp;</div><div class="crayon-line" id="crayon-5c2da9c3bf5ac440116535-2"><span class="crayon-sy">.</span><span class="crayon-o">/</span><span class="crayon-i">img</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5ac440116535-3">├──<span class="crayon-h"> </span><span class="crayon-v">gka_1</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5ac440116535-4">├──<span class="crayon-h"> </span><span class="crayon-v">gka_2</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5ac440116535-5">├──<span class="crayon-h"> </span><span class="crayon-v">gka_3</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5ac440116535-6">└──<span class="crayon-h"> </span><span class="crayon-sy">.</span><span class="crayon-sy">.</span><span class="crayon-sy">.</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5ac440116535-7">&nbsp;</div></div></td>
					</tr>
				</table>
			</div>
		</div>
<!-- [Format Time: 0.0015 seconds] -->
</td>
</tr>
</tbody>
</table>
<p>使用 gka 命令及 &#8211;ratio 参数，生成 2 倍图动画</p>
<p></p><!-- Crayon Syntax Highlighter v_2.7.2_beta -->

		<div id="crayon-5c2da9c3bf5b3113588998" class="crayon-syntax crayon-theme-sublime-text crayon-font-courier-new crayon-os-pc print-yes notranslate" data-settings=" minimize scroll-mouseover" style=" margin-top: 1px; margin-bottom: 1px; font-size: 14px !important; line-height: 15px !important;">
		
			<div class="crayon-plain-wrap"></div>
			<div class="crayon-main" style="">
				<table class="crayon-table">
					<tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 14px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5c2da9c3bf5b3113588998-1">1</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b3113588998-2">2</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 14px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5c2da9c3bf5b3113588998-1"><span class="crayon-v">gka</span><span class="crayon-h"> </span><span class="crayon-c ">/workspace/i</span><span class="crayon-v">mg</span><span class="crayon-o">/</span><span class="crayon-h"> </span><span class="crayon-o">--</span><span class="crayon-i">ratio</span><span class="crayon-h"> </span><span class="crayon-cn">2</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b3113588998-2">&nbsp;</div></div></td>
					</tr>
				</table>
			</div>
		</div>
<!-- [Format Time: 0.0003 seconds] -->
<p></p>
<table>
<thead>
<tr>
<th>文件夹：/workspace/gka-img-css-2x/</th>
</tr>
</thead>
<tbody>
<tr>
<td><!-- Crayon Syntax Highlighter v_2.7.2_beta -->

		<div id="crayon-5c2da9c3bf5b5965128933" class="crayon-syntax crayon-theme-sublime-text crayon-font-courier-new crayon-os-pc print-yes notranslate" data-settings=" minimize scroll-mouseover" style=" margin-top: 1px; margin-bottom: 1px; font-size: 14px !important; line-height: 15px !important;">
		
			<div class="crayon-plain-wrap"></div>
			<div class="crayon-main" style="">
				<table class="crayon-table">
					<tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 14px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-1">1</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-2">2</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-3">3</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-4">4</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-5">5</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-6">6</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-7">7</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-8">8</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-9">9</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-10">10</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b5965128933-11">11</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 14px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-1">&nbsp;</div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-2"><span class="crayon-sy">.</span><span class="crayon-o">/</span><span class="crayon-v">gka</span><span class="crayon-o">-</span><span class="crayon-v">img</span><span class="crayon-o">-</span><span class="crayon-v">css</span><span class="crayon-o">-</span><span class="crayon-cn">2x</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-3">└──<span class="crayon-h"> </span><span class="crayon-v">gka</span><span class="crayon-sy">.</span><span class="crayon-i">html</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-4">└──<span class="crayon-h"> </span><span class="crayon-v">gka</span><span class="crayon-sy">.</span><span class="crayon-i">css</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-5">└──<span class="crayon-h"> </span><span class="crayon-i">img</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-6"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span>└──<span class="crayon-h"> </span><span class="crayon-cn">2x</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-7"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_1</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-8"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_2</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-9"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_3</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-10"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>└──<span class="crayon-h"> </span><span class="crayon-sy">.</span><span class="crayon-sy">.</span><span class="crayon-sy">.</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b5965128933-11">&nbsp;</div></div></td>
					</tr>
				</table>
			</div>
		</div>
<!-- [Format Time: 0.0012 seconds] -->
</td>
</tr>
</tbody>
</table>
<p>生成的代码中将会把2倍图大小的图片，进行正常的1倍展示，使得帧动画在retina屏下能够清晰展示。</p>
<h2>方式二：对多文件夹图片进行处理</h2>
<p>举例，图片文件夹地址为 /workspace/img/ 中包含 1 倍图和 2 倍图的图片文件夹 name@1x，name@2x</p>
<table>
<thead>
<tr>
<th>文件夹：/workspace/img/</th>
</tr>
</thead>
<tbody>
<tr>
<td><!-- Crayon Syntax Highlighter v_2.7.2_beta -->

		<div id="crayon-5c2da9c3bf5b8062426452" class="crayon-syntax crayon-theme-sublime-text crayon-font-courier-new crayon-os-pc print-yes notranslate" data-settings=" minimize scroll-mouseover" style=" margin-top: 1px; margin-bottom: 1px; font-size: 14px !important; line-height: 15px !important;">
		
			<div class="crayon-plain-wrap"></div>
			<div class="crayon-main" style="">
				<table class="crayon-table">
					<tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 14px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-1">1</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-2">2</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-3">3</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-4">4</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-5">5</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-6">6</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-7">7</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-8">8</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-9">9</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-10">10</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-11">11</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-12">12</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5b8062426452-13">13</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 14px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-1">&nbsp;</div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-2"><span class="crayon-sy">.</span><span class="crayon-o">/</span><span class="crayon-i">img</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-3"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span>└──<span class="crayon-h"> </span><span class="crayon-r">name</span><span class="crayon-sy">@</span><span class="crayon-cn">1x</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-4"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_1</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-5"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_2</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-6"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_3</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-7"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>└──<span class="crayon-h"> </span><span class="crayon-sy">.</span><span class="crayon-sy">.</span><span class="crayon-sy">.</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-8"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span>└──<span class="crayon-h"> </span><span class="crayon-r">name</span><span class="crayon-sy">@</span><span class="crayon-cn">2x</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-9"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_1</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-10"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_2</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-11"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_3</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-12"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>└──<span class="crayon-h"> </span><span class="crayon-sy">.</span><span class="crayon-sy">.</span><span class="crayon-sy">.</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5b8062426452-13">&nbsp;</div></div></td>
					</tr>
				</table>
			</div>
		</div>
<!-- [Format Time: 0.0014 seconds] -->
</td>
</tr>
</tbody>
</table>
<p>使用下方命令，gka 将自动识别文件夹名(1x 为 1 倍图的目录，2x 为 2 倍图的目录，依此类推。)，一键生成 1 倍图和 2 倍图动画。并在不同的设备下自动选择播放对应动画，保持清晰。</p>
<p></p><!-- Crayon Syntax Highlighter v_2.7.2_beta -->

		<div id="crayon-5c2da9c3bf5ba631398110" class="crayon-syntax crayon-theme-sublime-text crayon-font-courier-new crayon-os-pc print-yes notranslate" data-settings=" minimize scroll-mouseover" style=" margin-top: 1px; margin-bottom: 1px; font-size: 14px !important; line-height: 15px !important;">
		
			<div class="crayon-plain-wrap"></div>
			<div class="crayon-main" style="">
				<table class="crayon-table">
					<tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 14px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5c2da9c3bf5ba631398110-1">1</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5ba631398110-2">2</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 14px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5c2da9c3bf5ba631398110-1"><span class="crayon-v">gka</span><span class="crayon-h"> </span><span class="crayon-c ">/workspace/i</span><span class="crayon-v">mg</span><span class="crayon-o">/</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5ba631398110-2">&nbsp;</div></div></td>
					</tr>
				</table>
			</div>
		</div>
<!-- [Format Time: 0.0002 seconds] -->
<p></p>
<table>
<thead>
<tr>
<th>文件夹：/workspace/gka-img-css/</th>
</tr>
</thead>
<tbody>
<tr>
<td><!-- Crayon Syntax Highlighter v_2.7.2_beta -->

		<div id="crayon-5c2da9c3bf5bd510832361" class="crayon-syntax crayon-theme-sublime-text crayon-font-courier-new crayon-os-pc print-yes notranslate" data-settings=" minimize scroll-mouseover" style=" margin-top: 1px; margin-bottom: 1px; font-size: 14px !important; line-height: 15px !important;">
		
			<div class="crayon-plain-wrap"></div>
			<div class="crayon-main" style="">
				<table class="crayon-table">
					<tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 14px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-1">1</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-2">2</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-3">3</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-4">4</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-5">5</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-6">6</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-7">7</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-8">8</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-9">9</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-10">10</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-11">11</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-12">12</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-13">13</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-14">14</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bd510832361-15">15</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 14px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-1">&nbsp;</div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-2"><span class="crayon-sy">.</span><span class="crayon-o">/</span><span class="crayon-v">gka</span><span class="crayon-o">-</span><span class="crayon-v">img</span><span class="crayon-o">-</span><span class="crayon-i">css</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-3">└──<span class="crayon-h"> </span><span class="crayon-v">gka</span><span class="crayon-sy">.</span><span class="crayon-i">html</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-4">└──<span class="crayon-h"> </span><span class="crayon-v">gka</span><span class="crayon-sy">.</span><span class="crayon-i">css</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-5">└──<span class="crayon-h"> </span><span class="crayon-i">img</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-6"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_1</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-7"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_2</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-8"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_3</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-9"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span>└──<span class="crayon-h"> </span><span class="crayon-sy">.</span><span class="crayon-sy">.</span><span class="crayon-sy">.</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-10"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span>└──<span class="crayon-h"> </span><span class="crayon-cn">2x</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-11"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_1</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-12"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_2</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-13"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>├──<span class="crayon-h"> </span><span class="crayon-v">gka_3</span><span class="crayon-sy">.</span><span class="crayon-i">png</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-14"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>└──<span class="crayon-h"> </span><span class="crayon-sy">.</span><span class="crayon-sy">.</span><span class="crayon-sy">.</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bd510832361-15">&nbsp;</div></div></td>
					</tr>
				</table>
			</div>
		</div>
<!-- [Format Time: 0.0014 seconds] -->
</td>
</tr>
</tbody>
</table>
<h2>其他方式</h2>
<p>结合 gka 提供的其他参数一同使用，如  -u 进行图片去重，-s 进行合图处理等等</p>
<p></p><!-- Crayon Syntax Highlighter v_2.7.2_beta -->

		<div id="crayon-5c2da9c3bf5bf722897044" class="crayon-syntax crayon-theme-sublime-text crayon-font-courier-new crayon-os-pc print-yes notranslate" data-settings=" minimize scroll-mouseover" style=" margin-top: 1px; margin-bottom: 1px; font-size: 14px !important; line-height: 15px !important;">
		
			<div class="crayon-plain-wrap"></div>
			<div class="crayon-main" style="">
				<table class="crayon-table">
					<tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 14px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5c2da9c3bf5bf722897044-1">1</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5bf722897044-2">2</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 14px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5c2da9c3bf5bf722897044-1"><span class="crayon-v">gka</span><span class="crayon-h"> </span><span class="crayon-c ">/workspace/i</span><span class="crayon-v">mg</span><span class="crayon-o">/</span><span class="crayon-h"> </span><span class="crayon-o">--</span><span class="crayon-i">ratio</span><span class="crayon-h"> </span><span class="crayon-cn">2</span><span class="crayon-h"> </span><span class="crayon-o">-</span><span class="crayon-i">us</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5bf722897044-2">&nbsp;</div></div></td>
					</tr>
				</table>
			</div>
		</div>
<!-- [Format Time: 0.0003 seconds] -->
<p></p>
<h1>多倍图帧动画原理</h1>
<p>当背景图片设置 background-size 为具体值时，图片将以该值的大小进行填充展示。二倍图的处理其实就是按照这个原理来实现的。举个例子，二倍图的宽高为80px 60px，那么可以通过缩小一倍，即设置 background-size 为 40px 30px 来得到展示中需要的宽高，这样在 retina 屏幕下，图片将保持清晰。示例代码如下</p>
<p></p><!-- Crayon Syntax Highlighter v_2.7.2_beta -->

		<div id="crayon-5c2da9c3bf5c1748878724" class="crayon-syntax crayon-theme-sublime-text crayon-font-courier-new crayon-os-pc print-yes notranslate" data-settings=" minimize scroll-mouseover" style=" margin-top: 1px; margin-bottom: 1px; font-size: 14px !important; line-height: 15px !important;">
		
			<div class="crayon-plain-wrap"></div>
			<div class="crayon-main" style="">
				<table class="crayon-table">
					<tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 14px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5c2da9c3bf5c1748878724-1">1</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5c1748878724-2">2</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5c1748878724-3">3</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5c1748878724-4">4</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5c1748878724-5">5</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5c1748878724-6">6</div><div class="crayon-num" data-line="crayon-5c2da9c3bf5c1748878724-7">7</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 14px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5c2da9c3bf5c1748878724-1"><span class="crayon-ta">&lt;style&gt;</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5c1748878724-2"><span class="crayon-k ">.bg </span><span class="crayon-sy">{</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5c1748878724-3"><span class="crayon-h">&nbsp;&nbsp;</span><span class="crayon-e ">background-size</span><span class="crayon-sy">:</span><span class="crayon-h"> </span><span class="crayon-i ">40px</span><span class="crayon-h"> </span><span class="crayon-i ">30px</span><span class="crayon-sy">;</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5c1748878724-4"><span class="crayon-h">&nbsp;&nbsp;</span><span class="crayon-e ">background</span><span class="crayon-sy">:</span><span class="crayon-h"> </span><span class="crayon-i ">url</span><span class="crayon-sy">(</span><span class="crayon-i ">./img.png</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5c1748878724-5"><span class="crayon-ta">&lt;/style&gt;</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5c1748878724-6"><span class="crayon-o">&lt;</span><span class="crayon-e">div </span><span class="crayon-t">class</span><span class="crayon-o">=</span><span class="crayon-s">"bg"</span><span class="crayon-o">&gt;</span><span class="crayon-o">&lt;</span><span class="crayon-o">/</span><span class="crayon-v">div</span><span class="crayon-o">&gt;</span></div><div class="crayon-line" id="crayon-5c2da9c3bf5c1748878724-7">&nbsp;</div></div></td>
					</tr>
				</table>
			</div>
		</div>
<!-- [Format Time: 0.0010 seconds] -->
<p></p>
<p>当图片是取自合图时，可以通过 background-position 来定位到图片在合图中的位置。而当设置 2 倍图的 background-size 进行 1 倍展示时，我们将需要把对应的 background-position 也进行对应的缩小倍数处理。紧接着就是大量的计算与代码编写了。</p>
<p>这一切，就交给 <a rel="nofollow" href="https://github.com/gkajs/gka">gka</a> 来处理吧！</p>
<p>欢迎使用 gka ，欢迎任何意见或建议，谢谢 ：D</p>
<p>GitHub: <a rel="nofollow" href="https://github.com/gkajs/gka">https://github.com/gkajs/gka</a></p>

        </div> 

                <!-- 打赏功能 -->
                <!-- <div class="paycode-wording">如果你觉得我们Alloyteam团队的博客和开源项目给你带来价值，可以通过捐赏支持我们，有你的支持，我们会做得更好！</div> -->
                <!-- <a class="helpus" href='javascript:;' title="支持原创文章 & 开源项目，请我们喝杯咖啡吧^_Q"> -->
                    <!-- <div class="paycode"> -->
                        <!-- <div class="wechatpay">微信扫一扫赞赏</div> -->
                        <!-- <div class="alipay">支付宝扫一扫赞赏</div> -->
                        <!-- <br />
                        <img src="images/wechatpaycode.png" />
                        <br /><br />
                        <img src="images/wechatpaycode.png" /> -->
                    <!-- </div> -->
                <!-- </a> -->
        </div>
        <div class="post-cp">
            
        <p class="cp-title">原创文章转载请注明：</p>
        <p class="cp-text">转载自AlloyTeam：<a href="http://www.alloyteam.com/2018/04/gka-ratio/">http://www.alloyteam.com/2018/04/gka-ratio/</a></p>
        </div>
        <div class="toolbar">
            <!-- <a class="helpus" href='javascript:;' title="支持原创文章 & 开源项目，请我们喝杯咖啡吧^_Q">
                <div class="paycode">
                    <div>　　如果你觉得我们Alloyteam团队的博客和开源项目给你带来价值，可以通过捐赏支持我们，有你的支持，我们会做得更好！</div>
                    <br />
                    <div class="wechatpay"></div>
                    <br />
                    <div class="alipay"></div>
                    
                </div>
            </a> -->
            <a class="helpus2" href='javascript:;' >
                <div class="paycode">
                    <div style="display: -webkit-box;margin: auto;width: 400px;">
                        <div class="wechatpay"></div>
                        <div class="alipay"></div>
                    </div>
                    
                    <!-- <img src="images/wechatpaycode.png" />
                    <img src="images/alipaycode.png" / >-->
                    <div>如果你觉得我们Alloyteam团队的博客和开源项目给你带来价值，可以通过捐赏支持我们<br />有你的支持，我们会做得更好！</div>
                </div>
            </a>
        </div>
        <div class="bshare-custom icon-medium-plus"><a title="分享到:" href="http://www.bShare.cn/" id="bshare-shareto" class="bshare-more">分享到:</a><a title="分享到QQ空间" class="bshare-qzone"></a><a title="分享到微信" class="bshare-weixin"></a><a title="分享到腾讯微博" class="bshare-qqmb"></a><a title="分享到新浪微博" class="bshare-sinaminiblog"></a><a title="更多平台" class="bshare-more bshare-more-icon more-style-addthis"></a><span class="BSHARE_COUNT bshare-share-count">0</span></div><script type="text/javascript" charset="utf-8" src="http://static.bshare.cn/b/buttonLite.js#style=-1&amp;uuid=&amp;pophcol=1&amp;lang=zh"></script><script type="text/javascript" charset="utf-8" src="http://static.bshare.cn/b/bshareC0.js"></script>
        </div>
    	    	<div id="comments" class="comments">
     <script type="text/javascript"> 
	var defaultAuthor = "称呼(必填)";
	var defaultEmail = "邮箱(不会被公开,必填)";
	var defaultUrl = "网站";
	var defaultComment = "评论内容...";
	
	function commentform_submit(){
		if(document.commentform.author.value == '' || document.commentform.author.value == defaultAuthor) {alert('咳咳...称呼忘填了');document.commentform.author.focus();return;}
		if(document.commentform.email.value == '' || document.commentform.email.value == defaultEmail) {alert('email...您的email没填');document.commentform.email.focus();return;}
		if(document.commentform.comment.value == '' || document.commentform.comment.value == defaultComment) {alert('评论内容在哪？');document.commentform.comment.focus();return;}
		if(document.commentform.url.value == defaultUrl) document.commentform.url.value = '';
		// document.commentform.submit();
	}
	</script>

		
<div class="clearfix"></div>


	<div id="respond" class="commentform">
		<h3>发表评论</h3>
		<div class="cancel-comment-reply"><a rel="nofollow" id="cancel-comment-reply-link" href="/2018/04/gka-ratio/#respond" style="display:none;">点击这里取消回复。</a></div>
				<form action="http://www.alloyteam.com/wp-comments-post.php" method="post" id="commentform">
		
						<p><input type="text" name="author" id="author" value="" size="22" tabindex="1" />
			<label for="author"><small>称呼 (必填)</small></label></p>
			<p><input type="text" name="email" id="email" value="" size="22" tabindex="2" />
			<label for="email"><small>邮箱 (不会被公开,必填)</small></label></p>
			<p><input type="text" name="url" id="url" value="" size="22" tabindex="3" />
			<label for="url"><small>网站</small></label></p>
						<p><textarea name="comment" id="comment" cols="100%" rows="6" tabindex="4" onkeydown="if(event.ctrlKey&amp;&amp;event.keyCode==13){document.getElementById('submit').click();return false};"></textarea></p>
			<p><input name="submit" type="submit" id="submit" tabindex="5" value="提 交" /><input type='hidden' name='comment_post_ID' value='13371' id='comment_post_ID' />
<input type='hidden' name='comment_parent' id='comment_parent' value='0' />
</p>
			<p style="display: none;"><input type="hidden" id="akismet_comment_nonce" name="akismet_comment_nonce" value="4d854af6b0" /></p><p style="display: none;"><input type="hidden" id="ak_js" name="ak_js" value="45"/></p>			
		</form>
				
	</div>
	
</div>
	</div>
</div>
<div id="sidebar">
	<div class="widget">			<div class="textwidget"><!-- 打赏功能 -->

<style type="text/css">
.helpus{
	display:none;

	margin: 20px auto;
	text-decoration:none;
	color:white;
	font-size:12px;
	line-height:1.8;
	
	background: url(/wp-content/uploads/2017/03/paybutton2.png) no-repeat center  #fff;
	background-size:cover;
	width: 219px;
	height: 80px;
border:1px solid rgba(0,0,0,0);
	border-radius: 10px;
	
	
}
.helpus:hover{
	border-radius: 10px 10px 0 0;
	color:white;
}
.helpus .paycode{
	display:none;
	position:relative;
	z-index:100;
	margin: 80px 0 0 0px;
	padding:10px;


	width:200px;

	background:#cd533d;
	overflow:hidden;
	
}

.helpus:hover .paycode{
	display:block;
}

.helpus .paycode img{
	width:200px;
}

</style>

<a class="helpus" href='javascript:;' title="支持原创文章 & 开源项目，请我们喝杯咖啡吧^_Q">
	<div class="paycode">
		<div>　　如果你觉得我们Alloyteam团队的博客和开源项目给你带来价值，可以通过捐赏支持我们，有你的支持，我们会做得更好！</div>
<br />
		<img src="/wp-content/uploads/2017/03/wechatpaycode.png" />
		<br /><br />
		<img src="/wp-content/uploads/2017/03/alipaycode.png" />
		
	</div>
</a></div>
		</div><div class="widget">			<div class="textwidget"><!-- TFC2017 -->
<a href="http://tfc.qq.com" target="_blank" style="position: relative; display: block; margin-bottom: 6px;position:relative;" title="了解腾讯前端大会">
    <img src="http://www.alloyteam.com/wp-content/uploads/2017/05/Group1.png" style="width:220px;height:88px;border-radius:3px;margin-top:8px;"><img src="http://cdn.alloyteam.com/assets/img/hot-32d141.png" style="position:absolute;width:38px;top:0;left:7px;">
</a></div>
		</div><div class="widget">			<div class="textwidget"><!-- CodeTank -->

<a href="http://codetank.alloyteam.com/" target="_blank" alt="点击跳转到CodeTank" title="点击跳转到CodeTank">
<div style="font-size:42px;
text-align: center;
color: #FF9D20;
margin: 0;
font-family: 'Segoe UI Light','Segoe UI','Microsoft Jhenghei','微软雅黑',sans-serif;">
<span style="color: #3C92FF;">Code</span>Tank</div>
<div style="text-align:center;">
<p>腾讯CodeTank</p>
<p>代码坦克</p>
</div>
</a></div>
		</div><div class="widget">			<div class="textwidget"><!-- 周刊入口 -->
<a href="http://www.alloyteam.com/alloyshare/weekly/p/latest" target="_blank" style="position: relative; display: block; margin-top: 10px;    height: 100px;
    overflow: hidden;border-radius:3px;" title="点击查阅Alloy周刊">
    <img src="http://www.alloyteam.com/wp-content/uploads/2017/04/01322.jpg" style="margin-top:-4px;">
    <div style="position: absolute; bottom: 9px; left: 14px">
        <div style="position: absolute; bottom: 0; left: 0; width: 40px; height: 40px; background-image: url(data:image/png;base64,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); background-repeat: no-repeat; background-size: contain; background-position: 50%; background-color: transparent;"></div>
        <div style="padding-left: 45px; background-color: transparent; color: #fff; font-size: 22px; font-weight: 700; text-shadow: 2px 2px #333;">Alloy周刊</div>
    </div>
</a></div>
		</div><div class="widget">			<div class="textwidget"><!-- 二维码 -->

<div style="width:220px;margin:10px  auto;position:relative;height:140px;font-size:12px;color:#444;text-align:center;">
<div style="position:absolute;top:0;left:0;width:50%;">
<img src="http://www.alloyteam.com/wp-content/uploads/2017/01/weixin.png" width=100 height=100 style="display:block;margin:0 auto 5px;" alt="公众号：AlloyTeam" title="公众号：AlloyTeam">

<div>扫码关注<br/>公众号:AlloyTeam</div>
</div>

<div style="display:block;position:absolute;top:0;right:0;width:50%;">
<a  target="_blank" href="http://shang.qq.com/wpa/qunwpa?idkey=6ae26f614ccf38b5495b20e80714a45b97e3146b0e61754b42f91a64bf7526f5" style="display:block;height:100px;margin:0 auto 5px;cursor:pointer;">
<img border=0 src="http://www.alloyteam.com/wp-content/uploads/2017/01/qun.png" width=100 height=100 alt="QQ公众群：162225981" title="QQ公众群：162225981"></a>

<div>扫码或点击加入QQ<br />
    <a  target="_blank" href="http://shang.qq.com/wpa/qunwpa?idkey=6ae26f614ccf38b5495b20e80714a45b97e3146b0e61754b42f91a64bf7526f5" style="display:block;height:100px;margin:0 auto 5px;cursor:pointer;">公众群:162225981</a>
</div>
</div>

</div></div>
		</div><div class="widget">			<div class="textwidget"><!--已经注释掉，qq群-->

<!-- <a target="_blank" href="http://shang.qq.com/wpa/qunwpa?idkey=6ae26f614ccf38b5495b20e80714a45b97e3146b0e61754b42f91a64bf7526f5"><img border="0" src="http://www.alloyteam.com/wp-content/uploads/2014/03/11.jpg" alt="点击加入AlloyTeam公众群" title="点击加入AlloyTeam公众群"></a>
<a target="_blank" href="http://shang.qq.com/wpa/qunwpa?idkey=6ae26f614ccf38b5495b20e80714a45b97e3146b0e61754b42f91a64bf7526f5" style="text-align: center;" alt="点击加入AlloyTeam公众群" title="点击加入AlloyTeam公众群">
<p>AlloyTeam公众群</p>
<p>群号：162225981</p>
</a> -->
</div>
		</div><div class="widget"><div class="ilovertitle"><span class="ilovertitlespan">分类目录</span></div>		<ul>
	<li class="cat-item cat-item-102"><a href="http://www.alloyteam.com/alloylabs/" title="腾讯 Web 前端 Alloy Labs 实验室">Alloy 实验室</a> (45)
<ul class='children'>
	<li class="cat-item cat-item-82"><a href="http://www.alloyteam.com/alloylabs/html5game/" title="开发HTML5游戏
">HTML5游戏</a> (14)
</li>
	<li class="cat-item cat-item-37"><a href="http://www.alloyteam.com/alloylabs/showcase/" >作品</a> (33)
</li>
</ul>
</li>
	<li class="cat-item cat-item-4"><a href="http://www.alloyteam.com/webdevelop/" title="Web前端开发技术">Web开发</a> (495)
<ul class='children'>
	<li class="cat-item cat-item-6"><a href="http://www.alloyteam.com/webdevelop/css3/" >CSS3</a> (32)
</li>
	<li class="cat-item cat-item-20"><a href="http://www.alloyteam.com/webdevelop/html5/" >HTML5</a> (61)
</li>
	<li class="cat-item cat-item-5"><a href="http://www.alloyteam.com/webdevelop/javascript/" >JavaScript</a> (97)
</li>
	<li class="cat-item cat-item-237"><a href="http://www.alloyteam.com/webdevelop/node/" title="Node.js相关的文章">Node.js</a> (23)
</li>
	<li class="cat-item cat-item-63"><a href="http://www.alloyteam.com/webdevelop/web-%e5%89%8d%e7%ab%af%e4%bc%98%e5%8c%96/" >Web 前端优化</a> (33)
</li>
	<li class="cat-item cat-item-38"><a href="http://www.alloyteam.com/webdevelop/web-%e5%89%8d%e7%ab%af%e8%b5%84%e8%ae%af/" >Web 前端资讯</a> (49)
</li>
	<li class="cat-item cat-item-1"><a href="http://www.alloyteam.com/webdevelop/ued/" title="用户体验设计、可用性研究、以用户为中心的设计">用户体验设计</a> (18)
</li>
	<li class="cat-item cat-item-273"><a href="http://www.alloyteam.com/webdevelop/%e7%bb%8f%e9%aa%8c%e5%bf%83%e5%be%97/" >经验心得</a> (13)
</li>
</ul>
</li>
	<li class="cat-item cat-item-11"><a href="http://www.alloyteam.com/team/" >团队</a> (31)
</li>
	<li class="cat-item cat-item-217"><a href="http://www.alloyteam.com/mobiledevelop/" >移动开发</a> (25)
<ul class='children'>
	<li class="cat-item cat-item-251"><a href="http://www.alloyteam.com/mobiledevelop/android/" title="Android 开发技术">Android 开发</a> (8)
</li>
	<li class="cat-item cat-item-252"><a href="http://www.alloyteam.com/mobiledevelop/ios-develop/" title="iOS 开发技术">iOS 开发</a> (1)
</li>
	<li class="cat-item cat-item-253"><a href="http://www.alloyteam.com/mobiledevelop/mobileweb/" title="移动 Web 开发技术">移动 Web 开发</a> (13)
</li>
</ul>
</li>
	<li class="cat-item cat-item-39"><a href="http://www.alloyteam.com/%e8%b5%84%e6%ba%90%e5%b7%a5%e5%85%b7/" >资源工具</a> (53)
</li>
		</ul>
</div><div class="widget"><div class="ilovertitle"><span class="ilovertitlespan">最新文章</span></div><ul id="recentcomments"><li class="recentcomments"><span class="comment-author-link">godaangel</span>发表在《<a href="http://www.alloyteam.com/2017/03/moves-the-input-box-fill-series-a/comment-page-1/#comment-261388">移动端输入框填坑系列（一）</a>》</li><li class="recentcomments"><span class="comment-author-link">橙子先生</span>发表在《<a href="http://www.alloyteam.com/2018/03/13344/comment-page-1/#comment-261387">要做软件工程师，而不是前端工程师</a>》</li><li class="recentcomments"><span class="comment-author-link"><a href='https://cpselvis.github.io/' rel='external nofollow' class='url'>cpselvis</a></span>发表在《<a href="http://www.alloyteam.com/2016/02/code-split-by-routes/comment-page-1/#comment-261376">在Webpack中使用Code Splitting实现按需加载</a>》</li><li class="recentcomments"><span class="comment-author-link">yee</span>发表在《<a href="http://www.alloyteam.com/2016/03/node-embedded-database-nedb/comment-page-1/#comment-261373">Node嵌入式数据库——NeDB</a>》</li><li class="recentcomments"><span class="comment-author-link">crazyming</span>发表在《<a href="http://www.alloyteam.com/message-board/comment-page-20/#comment-261370">留言板</a>》</li><li class="recentcomments"><span class="comment-author-link"><a href='http://jianpage.com' rel='external nofollow' class='url'>ixx</a></span>发表在《<a href="http://www.alloyteam.com/2017/08/13065/comment-page-1/#comment-261343">AlloyTeam ESLint 配置指南</a>》</li><li class="recentcomments"><span class="comment-author-link"><a href='http://nullno.com' rel='external nofollow' class='url'>冬冬</a></span>发表在《<a href="http://www.alloyteam.com/2015/08/2015-teng-xun-alloyteam-zhao-pin-web-qian-duan-gong-cheng-shi/comment-page-3/#comment-261324">2018·腾讯AlloyTeam招聘·Web+工程师</a>》</li><li class="recentcomments"><span class="comment-author-link">zz</span>发表在《<a href="http://www.alloyteam.com/2014/03/effect-js-css-and-img-event-of-domcontentloaded/comment-page-1/#comment-261232">JS、CSS以及img对DOMContentLoaded事件的影响</a>》</li><li class="recentcomments"><span class="comment-author-link">随意</span>发表在《<a href="http://www.alloyteam.com/2012/11/javascript-throttle/comment-page-2/#comment-261140">浅谈javascript的函数节流</a>》</li><li class="recentcomments"><span class="comment-author-link">肥翔</span>发表在《<a href="http://www.alloyteam.com/2015/09/explore-performance/comment-page-1/#comment-261097">初探 performance &#8211; 监控网页与程序性能</a>》</li></ul></div><div class="widget"><div class="ilovertitle"><span class="ilovertitlespan">合作伙伴</span></div>			<div class="textwidget"><!-- HTML5梦工场 -->

<a target="_blank" href="http://www.html5dw.com"  style="display: block;margin: 10px auto;text-align: center;">
<img style="display: block;margin:auto;”  border="0" src="http://www.alloyteam.com/wp-content/uploads/2017/01/h5dreamworks40.png" alt="HTML5梦工场" title="HTML5梦工场">
HTML5梦工场</a>
</div>
		</div><div class="widget">			<div class="textwidget"><!-- 腾讯云 -->

<a target="_blank" href="http://www.qcloud.com/redirect.php?redirect=1001&cps_key=50b46969b6fa53f1334070ccf5a941d0"  style="display: block;margin: auto;width: 150px;text-align: center;">
<img  border="0" src="http://www.alloyteam.com/wp-content/uploads/2015/07/logo-e1485056491948.png" alt="腾讯云" title="托管于腾讯云">
</a>
<a target="_blank" href="http://www.qcloud.com/redirect.php?redirect=1001&cps_key=50b46969b6fa53f1334070ccf5a941d0" style="display: block;margin: auto;width: 160px;text-align: center;">推荐使用腾讯云</a>
</div>
		</div><div class="widget">			<div class="textwidget"><!-- Coding -->


<a target="_blank" href="https://coding.net/" style="display: block;margin: 10px auto;width:150px;text-align: center;"><img border="0" src="http://www.alloyteam.com/wp-content/uploads/2016/09/codnig.jpg" alt="Coding" title="将代码托管于Coding">推荐使用 Coding.net</a>
</div>
		</div><div class="widget"><div class="ilovertitle"><span class="ilovertitlespan">兄弟团队</span></div>
	<ul class='xoxo blogroll'>
<li><a href="http://cdc.tencent.com" target="_blank">腾讯 CDC</a></li>
<li><a href="http://isux.tencent.com/" target="_blank">腾讯 ISUX</a></li>
<li><a href="http://tgideas.qq.com/" target="_blank">腾讯游戏 TGideas</a></li>
<li><a href="http://qqfe.org" target="_blank">腾讯 FERD</a></li>
<li><a href="http://efe.baidu.com" target="_blank">百度前端 EFE</a></li>
<li><a href="http://fex.baidu.com/" target="_blank">百度前端 FEX</a></li>
<li><a href="http://taobaofed.org/" target="_blank">淘宝前端团队 FED</a></li>
<li><a href="http://MelonTeam.com" rel="co-worker" target="_blank">腾讯 MelonTeam</a></li>

	</ul>
</div>
<div class="widget"><div class="ilovertitle"><span class="ilovertitlespan">友情链接</span></div>
	<ul class='xoxo blogroll'>
<li><a href="https://docschina.org" title="http://www.alloyteam.com/wp-content/uploads/2017/08/印记中文logo-white.png" target="_blank">印记中文</a></li>
<li><a href="http://www.iwebxy.com/?type=alloyteam" rel="acquaintance" target="_blank">iWeb学院</a></li>
<li><a href="http://www.w3ctech.com/" target="_blank">W3CTech</a></li>
<li><a href="http://www.qianduan.net/" target="_blank">前端观察</a></li>
<li><a href="http://www.w3cplus.com/" target="_blank">W3C Plus</a></li>
<li><a href="http://www.css88.com" target="_blank">Web 前端开发</a></li>
<li><a href="http://dopro.io/about-us" target="_blank">腾讯Deep Ocean</a></li>
<li><a href="http://www.v2ex.com/" title="V2EX &#8211; 创意工作者们的社区" target="_blank">V2EX</a></li>
<li><a href="http://djt.qq.com" target="_blank">腾讯大讲堂</a></li>
<li><a href="http://www.blueidea.com/" target="_blank">蓝色理想</a></li>
<li><a href="http://www.html5cn.com.cn">HTML5中文学习网</a></li>
<li><a href="http://www.aseoe.com/" target="_blank">爱思资源网</a></li>
<li><a href="http://www.niudana.com" target="_blank">牛大拿_前端设计导航</a></li>
<li><a href="http://www.nihaoshijie.com.cn" target="_blank">吕小鸣前端博客</a></li>
<li><a href="http://daxue.qq.com/" rel="acquaintance" target="_blank">腾讯大学</a></li>

	</ul>
</div>

</div>
﻿ <div class="clearfix"></div>

</div>
</div>
<div id="footer">
	<div id="footerbar">
    <!--Copyright-->
		<div class="copyright"> 
			<p>
				<span>
					Copyright &copy;&nbsp; 2011-2018  <a href="http://www.alloyteam.com">AlloyTeam</a>. All Rights Reserved. Powered By <a href="http://wordpress.org/">WordPress</a>.
				</span>
			</p>
		</div>
    <!--Copyright End-->     
	</div>
<!--[if !IE]><!-->
<script type="text/javascript">
	window.onerror=function(){return true;}

	var alloyrefer = document.referrer;
	var hasClassListProperty = document && Object.prototype.hasOwnProperty.call(document.documentElement,'classList');
	var addClass = function(){
        if (hasClassListProperty) {
            return function (el, className) {
                if (!el || !className ) {
                    return;
                }
                el.classList.add(className);
            };
        } else {
            return function (el, className) {
                if (!el || !className ) {
                    return;
                }
                el.className += ' ' + className;
            };
        }
	}();
	var refername = "www.alloyteam.com";
	var flag = alloyrefer.indexOf(refername) === -1;
	if(flag && alloyrefer !== ""){	
		var main = document.getElementById("main");
		var alloyteam = document.getElementById("alloyteam");
		var alloyteam2 = document.getElementById("alloyteam2");
		var tencentInfo = document.getElementById("tencentInfo");
		var header = document.getElementById("header");	
		var alloy = document.getElementById("alloy");	
		addClass(alloy,'alloy'); 
		addClass(header,'header');		
		addClass(main,'main');
		addClass(alloyteam,'alloyteam');
		addClass(alloyteam2,'alloyteam');
		addClass(tencentInfo,'tencentInfo');

	}
	document.body.style.display = "block";
	if(flag){
		setTimeout(function(){
			if (navigator.userAgent.indexOf('Firefox') >= 0){
				document.documentElement.scrollTop = 1;
				document.documentElement.scrollTop = 0;
			}else{
				document.body.scrollTop = 2;
				document.body.scrollTop = 0;   
			}
				
		},3000);		
	}
</script>
<!--<![endif]-->  
<script type="text/javascript" src="http://www.alloyteam.com/wp-content/themes/alloyteam/js/all.js"></script>
<script src="//s.url.cn/pub/js/alloyreport.js?_bid=2231"></script>
<script type="text/javascript" src="http://www.alloyteam.com/wp-content/themes/alloyteam/js/report.js"></script>

<script type="text/javascript" src="http://www.alloyteam.com/wp-content/themes/alloyteam/comments-ajax.js"></script>
<div align="center"><small>Site is using the <a href="https://wordpress.org/plugins/seo-wizard/" title="Wordpress Seo" target="_blank">Seo Wizard</a> plugin by <a href="http://seo.uk.net/" target="_blank">http://seo.uk.net/</a></small></div>
<!-- Powered by WPtouch: 4.0.3 --><div id="su-footer-links" style="text-align: center;"></div><script type='text/javascript' src='http://www.alloyteam.com/wp-content/plugins/akismet/_inc/form.js?ver=3.2'></script>
<script type='text/javascript'>
/* <![CDATA[ */
var ajax_object = {"ajax_url":"http:\/\/www.alloyteam.com\/wp-admin\/admin-ajax.php"};
/* ]]> */
</script>
<script type='text/javascript' src='http://www.alloyteam.com/wp-content/plugins/seo-wizard/js/admin.js?ver=1.0.0'></script>
<script type='text/javascript' src='http://www.alloyteam.com/wp-content/plugins/seo-wizard/js/zeroclipboard/ZeroClipboard.js?ver=1.0.0'></script>
<script type='text/javascript'>
/* <![CDATA[ */
var viewsCacheL10n = {"admin_ajax_url":"http:\/\/www.alloyteam.com\/wp-admin\/admin-ajax.php","post_id":"13371"};
/* ]]> */
</script>
<script type='text/javascript' src='http://www.alloyteam.com/wp-content/plugins/wp-postviews/postviews-cache.js?ver=1.68'></script>
<script type='text/javascript' src='http://www.alloyteam.com/wp-content/plugins/dynamic-to-top/js/libs/jquery.easing.js?ver=1.3'></script>
<script type='text/javascript'>
/* <![CDATA[ */
var mv_dynamic_to_top = {"text":"To Top","version":"0","min":"300","speed":"300","easing":"easeInOutExpo","margin":"20"};
/* ]]> */
</script>
<script type='text/javascript' src='http://www.alloyteam.com/wp-content/plugins/dynamic-to-top/js/dynamic.to.top.min.js?ver=3.5'></script>
<script type='text/javascript' src='http://www.alloyteam.com/wp-includes/js/wp-embed.min.js?ver=4.7.2'></script>

</div>


<script type="text/javascript" src="http://tajs.qq.com/stats?sId=39379138" charset="UTF-8"></script>
</body>
</html>
"""

soup = BeautifulSoup(data, 'lxml')
item = {}
item['title'] = soup.find('a', 'blogTitle btitle').string
item['author'] = soup.find(rel='author').string

# 内容写入md后缀文件
content = soup.select(".content_banner > .text")[0]
md_text = html_to_md(content)
md_str = '\n'.join(md_text)
#print(md_str)
with open('text.md', 'w', encoding='utf-8') as f:
    f.write(md_str)

