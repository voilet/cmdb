/*
 * Translated default messages for the jQuery validation plugin.
 * Locale: CN
 */
jQuery.extend(jQuery.validator.messages, {
        required: "不能为空",
                remote: "请修正该字段",
                email: "电子邮件格式不正确",
                url: "网址格式不正确",
                date: "日期格式不正确",
                dateISO: "日期 格式(ISO)不正确",
                number: "请输入合法的数字",
                digits: "请输入整数",
                creditcard: "请输入合法的信用卡号",
                equalTo: "请再次输入相同的值",
                accept: "请输入拥有合法后缀名的字符串",
                maxlength: jQuery.validator.format("长度不能大于 {0} "),
                minlength: jQuery.validator.format("长度不能小于 {0} "),
                rangelength: jQuery.validator.format("长度需在 {0} 和 {1} 之间"),
                range: jQuery.validator.format("大于等于 {0}且小于等于 {1}"),
                max: jQuery.validator.format("最大值为 {0}"),
                min: jQuery.validator.format("最小值为 {0}")
});