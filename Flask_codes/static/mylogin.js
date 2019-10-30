// $.ajax({
//      //url:"{{url_for('/flask_json/',username={{username}})}}",
//      url:"http://localhost:5050/flask_json/"+'{{username}}',
//     type:"GET",
//   datatype:"application/json",
//   //成功的回调函数
//    success:function(data){
//    alert(data['username']+",好久不见~");
//    console.log(data.toString())
// },
//    //失败的回调函数
//    error:function(){
//    alert("服务器请求失败");
//    },
//
//     // //发送请求前调用，可以放一些“正在加载”之类的话
//     // beforeSend:function(){
//     // alert("正在加载");
//     // }
// });

<!--如果这里js直接写了函数如function申明,则会等待调用；如果是执行代码只有$.ajax,会直接执行。-->
<!--ajax请求可以模拟跨域,所以用ajax;url为请求的地址,没使用url_for反转得到url是因为参数argument不太适合用jinja2特殊标记语言-->
<!--datatype必须设置为application/json;为了和服务器端的flask_json()返回的json报文content-type保持一致,否则请求失败触犯error函数-->
<!--PS：上述的datatype问题对于C# web接口返回数据很重要;-->
<!--如果人家ajax请求的数据类型content-type是text/json,你服务器C#返回字符串拼接json,人家可以收到-->
<!--如果...............................是application/json,你服务器端C#返回json字符串就不行了,人家收到但是数据类型不一致,会走error部分-->
<!--此时就需要C#通过创建对象,然后对象转成json发出去即可-->
function ajaxAlert(argument) {
    $.ajax({
        url:"http://localhost:5050/flask_json/"+argument.toString(),
        type: 'GET',
        datatype:"application/json",
        success:function (data) {
            alert(data['username']+',好久不见啊~');
            console.log(data)
        },
        error:function () {
            alert('服务器请求失败!');
        }
    })

}