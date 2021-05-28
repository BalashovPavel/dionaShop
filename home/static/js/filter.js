function fun1() {
    var i;
    var list_product = document.getElementsByClassName("product-wrapper");
    /***************   ЦВЕТА   ***************/
    var chbox_white = document.getElementById("white");
    var white = document.getElementsByClassName("white");
    var chbox_black = document.getElementById("black");
    var black = document.getElementsByClassName("black");
    var chbox_green = document.getElementById("green");
    var green = document.getElementsByClassName("green");

    on_check(chbox_white, white, chbox_black, black, chbox_green, green);
    off_check(chbox_white, chbox_black, chbox_green);
    on_check(chbox_black, black, chbox_white, white, chbox_green, green);
    off_check(chbox_black, chbox_white, chbox_green);
    on_check(chbox_green, green, chbox_black, black, chbox_white, white);
    off_check(chbox_green, chbox_black, chbox_white);

    function multi(property) {
        for (i = 0; i < property.length; i++) {
            property[i].className = property[i].className.replace("false", "true");
        }
    }
    function if_on_check(check, prop) {
        if (check.checked) {
            multi(prop);
        }
    }
    function on_check(check0, prop0, check1, prop1, check2, prop2) {
        if (check0.checked) {
            for (i = 0; i < list_product.length; i++) {
                list_product[i].className = list_product[i].className.replace("true", "false");
            }
            if_on_check(check0, prop0);
            if_on_check(check1, prop1);
            if_on_check(check2, prop2);
        }
    }
    function off_check(check0, check1, check2) {
        if (check1.checked == false && check2.checked == false) {
            if (check0.checked == false) {
                for (i = 0; i < list_product.length; i++) {
                    list_product[i].className = list_product[i].className.replace("false", "true");
                }
            }
        }
    }
}

function fun2() {
    var i;
    var list_product = document.getElementsByClassName("product-wrapper");
    /***************   СТРАНА   ***************/
    var chbox_turkey = document.getElementById("turkey");
    var turkey = document.getElementsByClassName("turkey");
    var chbox_china = document.getElementById("china");
    var china = document.getElementsByClassName("china");
    var chbox_russia = document.getElementById("russia");
    var russia = document.getElementsByClassName("russia");

    on_check_cntr(chbox_turkey, turkey, chbox_china, china, chbox_russia, russia);
    off_check_cntr(chbox_turkey, chbox_china, chbox_russia);
    on_check_cntr(chbox_china, china, chbox_turkey, turkey, chbox_russia, russia);
    off_check_cntr(chbox_china, chbox_turkey, chbox_russia);
    on_check_cntr(chbox_russia, russia, chbox_china, china, chbox_turkey, turkey);
    off_check_cntr(chbox_russia, chbox_china, chbox_turkey);

    function multi_cntr(property) {
        for (i = 0; i < property.length; i++) {
            property[i].className = property[i].className.replace("fls_ctr", "tr_ctr");
        }
    }
    function if_on_check_cntr(check, prop) {
        if (check.checked) {
            multi_cntr(prop);
        }
    }
    function on_check_cntr(check0, prop0, check1, prop1, check2, prop2) {
        if (check0.checked) {
            for (i = 0; i < list_product.length; i++) {
                list_product[i].className = list_product[i].className.replace("tr_ctr", "fls_ctr");
            }
            if_on_check_cntr(check0, prop0);
            if_on_check_cntr(check1, prop1);
            if_on_check_cntr(check2, prop2);
        }
    }
    function off_check_cntr(check0, check1, check2) {
        if (check1.checked == false && check2.checked == false) {
            if (check0.checked == false) {
                for (i = 0; i < list_product.length; i++) {
                    list_product[i].className = list_product[i].className.replace("fls_ctr", "tr_ctr");
                }
            }
        }
    }
}






/*
function fun1() {
    var i;
    var list_product = document.getElementsByClassName("product-wrapper"); */

/***************   ЦВЕТА   ***************/
/*     var chbox_white = document.getElementById("white");
    var white = document.getElementsByClassName("white");
    var chbox_black = document.getElementById("black");
    var black = document.getElementsByClassName("black");

    on_check(chbox_white, white, chbox_black, black);
    off_check(chbox_white, chbox_black);
    on_check(chbox_black, black, chbox_white, white);
    off_check(chbox_black, chbox_white); */


/***************   СТРАНА   ***************/

/*    var chbox_turkey = document.getElementById("turkey");
   var turkey = document.getElementsByClassName("turkey");
   var chbox_china = document.getElementById("china");
   var china = document.getElementsByClassName("china");

   on_check(chbox_turkey, turkey, chbox_china, china);
   off_check(chbox_turkey, chbox_china);
   on_check(chbox_china, china, chbox_turkey, turkey);
   off_check(chbox_china, chbox_turkey);





   function multi(color) {
       for (i = 0; i < color.length; i++) {
           color[i].className = color[i].className.replace("false", "true");
       }
   }

   function on_check(check0, prop0, check1, prop1, check2, prop2) {
       if (check0.checked) {
           for (i = 0; i < list_product.length; i++) {
               list_product[i].className = list_product[i].className.replace("true", "false");
           }
           if (check0.checked) {
               multi(prop0);
           }
           if (check1.checked) {
               multi(prop1);
           }
           if (check2.checked) {
               multi(prop2);
           }
       }
   }

   function off_check(check_main, check1) {
       if (check1.checked == false) {
           if (check_main.checked == false) {
               for (i = 0; i < list_product.length; i++) {
                   list_product[i].className = list_product[i].className.replace("false", "true");
               }
           }
       }
   }
}
*/





