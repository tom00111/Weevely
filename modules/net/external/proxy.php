<?php
/**
 * Simple php proxy https://github.com/milovanderlinden/php-proxy
 * Slightly modified for weevely usage
 */
class proxyClass {
    var $DOMAIN;
    var $POSTURL;
    var $PURL=array();
    var $RESPONSE=array();

    public function __construct() {
        define(HOST,$_SERVER['SERVER_NAME'].$_SERVER['PHP_SELF']);
    }

    public function close() {
        unlink(session_id());
        session_destroy();
        header('Location: /');
    }

    public function query($U,$POST,$GET,$FILES,$COOKIE='') {
        if(count($POST)) {
            foreach($POST as $key => $value) {
                if($key!='u' && $key!='c') {
                    $POSTVARS.=$key."=".$value."&";
                }
            }
            if($POSTVARS) {
                $posted=1;
            }
        }

        if(count($FILES)) {
            $files=1;
            foreach($FILES as $key => $value) {
                $POSTVARS.=$key."=@".$value['tmp_name']."&";
            }
        }

        $POSTVARS=$POSTVARS?substr($POSTVARS,0,-1):'';
        $U=urldecode($U);
        if(!eregi('[.]+',$U)) {
            $U=base64_decode($U);
        }
        if(!eregi('^(http|ftp|https)',$U)) {
            $U='http://'.$U;
        }
        $this->POSTURL=$U;
        foreach($GET as $k=>$v) {

            if($k!='u' && $k!='c') {
                $this->POSTURL.='&'.$k.'='.$v;
            }
        }
        $this->POSTURL= str_replace(' ','%20',$this->POSTURL);

        $this->PURL=parse_url($U);
        $this->DOMAIN=$this->PURL['host'].$this->PURL['path'];

        if(ereg('.',$this->PURL['path'])) {
            $this->DOMAIN=ereg_replace('/[^\/]*$','',$this->DOMAIN);
        }
        define(PHOST,$this->PURL['host']);
        define(DOMAIN,$this->DOMAIN);
        $ch = curl_init($this->POSTURL);

        if($posted) {
            curl_setopt($ch, CURLOPT_POST,0);
        }
        curl_setopt($ch, CURLOPT_VERBOSE,0);
        curl_setopt($ch, CURLOPT_USERAGENT,$_SERVER['user-agent']);
        if($posted) curl_setopt($ch, CURLOPT_POSTFIELDS,$POSTVARS);
        if($files)  curl_setopt($ch, CURLOPT_UPLOAD,1);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION,1);
        curl_setopt($ch, CURLOPT_BINARYTRANSFER,1);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER,0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST,0);
        curl_setopt($ch, CURLOPT_REFERER,"http://".$this->DOMAIN);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT,0);
        curl_setopt($ch, CURLOPT_AUTOREFERER,0);
        curl_setopt($ch, CURLOPT_COOKIEJAR,'ses_'.session_id());
        curl_setopt($ch, CURLOPT_COOKIEFILE,'ses_'.session_id());
        if(strlen($COOKIE)>0) curl_setopt($ch, CURLOPT_COOKIE,$COOKIE);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
        curl_setopt($ch, CURLOPT_FAILONERROR,1);

        $this->CONTENT = curl_exec($ch);
        $this->RESPONSE=curl_getinfo($ch);
        curl_close($ch);
    }

    public function getPage() {
        if(ereg('html',$this->RESPONSE['content_type'])) {
            $this->get_html();
            $this->get_css();
        } elseif (ereg('image',$this->RESPONSE['content_type'])) {
            $this->get_image();
        } elseif (ereg('javascript',$this->RESPONSE['content_type'])) {
            $this->get_javascript();
        } elseif (ereg('css',$this->RESPONSE['content_type'])) {
            $this->get_css();
        } elseif (ereg('xml',$this->RESPONSE['content_type'])) {
            $this->RESPONSE['content_type'] ='text/xml';
            $this->get_plain();
        } else {
            $this->RESPONSE['content_type'] ='text/plain';
            $this->get_plain();
        }
        header("Content-Type: ".$this->RESPONSE['content_type']);
        if(eregi('image/([a-z]+)',$this->RESPONSE['content_type'],$type)) {
            $newImg = imagecreatefromstring($this->CONTENT);
            if($type[1]=="jpeg") {
                imagejpeg($newImg,'',100);
            }
            if($type[1]=="png") {
                imagegif($newImg,'',100);
            }
            if($type[1]=="gif") {
                imagepng($newImg,'',100);
            }
        } else {
            echo $this->CONTENT;
        }
    }

    public function get_file() {

    }

    public function get_image() {

    }

    public function get_javascript() {
        $patern=array(
                '/([\"]+)([^\"\s]*)([\"]+)/i',
                '/([\']+)([^\'\s]*)([\']+)/i'
        );
        function replace_js($m) {
            $d='';
            if(eregi('^\/',$m[2])) {
                $d='http://'.PHOST;
                $ok=1;
            } else {
                if(!eregi('^(htt|ftp)',$m[2]) && eregi('/',$m[2])) {
                    $d='http://'.DOMAIN.'/';
                    $ok=1;
                }
            }
            if($ok) {
                return $m[1].'http://'.HOST.'?u='.base64_encode($d.$m[2]).$m[1];
            } else {
                return $m[1].$m[2].$m[1];
            }

        }
        $this->CONTENT=preg_replace_callback($patern,"replace_js",$this->CONTENT);
    }

    public function get_css() {
        $patern=array(
                '/url\([\s]*[\'\"\`]?([^\)\s\'\"\`]+)[\'\"\`]?[\s]*\)/i'
        );
        function replace_css($m) {
            $d='';
            if(eregi('^\/',$m[1])) {
                $d='http://'.PHOST;
                $ok=1;
            } else {
                if(!eregi('^(htt|ftp)',$m[1])) {
                    $d='http://'.DOMAIN.'/';
                    $ok=1;
                } else {
                    $ok=1;
                }
            }

            if($ok) {
                return 'url(http://'.HOST.'?u='.base64_encode($d.$m[1]).')';
            }
        }
        $this->CONTENT=preg_replace_callback($patern,"replace_css",$this->CONTENT);
    }

    public function get_html() {
        $patern=array(
                '/[\s]+(src|href|url|location|background|action)[\s]*=[\s]*([\'\"\`])?[\s]*([^\'\"\`\s>]+)([\'\"\`>])?/i',
                '/([\"]+)(\/[^\"\s]*)([\"]+)/i',
                '/([\']+)(\/[^\'\s]*)([\']+)/i'
        );
        function replace_html($m) {
            $d='';
            if($m[1]=='"' || $m[1]=="'") {
                if(eregi('^\/',$m[2])) {
                    $d='http://'.PHOST;
                    $ok=1;
                } else {
                    if(!eregi('^(htt|ftp)',$m[2]) && eregi('/',$m[2])) {
                        $d='http://'.DOMAIN.'/';
                        $ok=1;
                    }
                }
                if($ok) {
                    return $m[1].'http://'.HOST.'?u='.base64_encode($d.$m[2]).$m[1];
                }
                else {
                    return $m[1].$m[2].$m[1];
                }

            } else {
                if($m[4]=='>') $e=">";
                if(eregi('^\/',$m[3])) {
                    $d='http://'.PHOST;
                } else {
                    if(!eregi('^(htt|ftp)',$m[3])) $d='http://'.DOMAIN.'/';
                }
                if(!ereg('^java',$m[3])) {
                    return ' '.$m[1].'="http://'.HOST.'?u='.base64_encode($d.$m[3]).'"'.$e;
                } else {
                    return ' '.$m[1].'="'.$m[3].'"';
                }
            }
        }
        $this->CONTENT=preg_replace_callback($patern,'replace_html',$this->CONTENT);
    }
    public function get_plain() {
        $patern=array(
                '/[\s]+(src|href|url|location|background|action)[\s]*=[\s]*([\'\"\`])?[\s]*([^\'\"\`\s>]+)([\'\"\`>])?/i',
                '/([\"]+)(\/[^\"\s]*)([\"]+)/i',
                '/([\']+)(\/[^\'\s]*)([\']+)/i'
        );
        function replace_html($m) {
            $d='';
            if($m[1]=='"' || $m[1]=="'") {
                if(eregi('^\/',$m[2])) {
                    $d='http://'.PHOST;
                    $ok=1;
                } else {
                    if(!eregi('^(htt|ftp)',$m[2]) && eregi('/',$m[2])) {
                        $d='http://'.DOMAIN.'/';
                        $ok=1;
                    }
                }
                if($ok) {
                    return $m[1].'http://'.HOST.'?u='.base64_encode($d.$m[2]).$m[1];
                }
                else {
                    return $m[1].$m[2].$m[1];
                }

            } else {
                if($m[4]=='>') $e=">";
                if(eregi('^\/',$m[3])) {
                    $d='http://'.PHOST;
                } else {
                    if(!eregi('^(htt|ftp)',$m[3])) $d='http://'.DOMAIN.'/';
                }
                if(!ereg('^java',$m[3])) {
                    return ' '.$m[1].'="http://'.HOST.'?u='.base64_encode($d.$m[3]).'"'.$e;
                } else {
                    return ' '.$m[1].'="'.$m[3].'"';
                }
            }
        }
        $this->CONTENT=preg_replace_callback($patern,'replace_html',$this->CONTENT);
    }
}

session_start();
$P=new proxyClass();
$P->query($_REQUEST['u'],$_POST,$_GET,$_FILES,$_POST['c']);
$P->getPage();

?>
