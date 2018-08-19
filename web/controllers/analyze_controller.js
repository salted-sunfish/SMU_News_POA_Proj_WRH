/**
 * Created by EVERCX on 2017/5/9.
 */

var fs = require('fs');
var exec = require('child_process').exec;
var filePath = './python/online_analyze.py';

var net = require('net');

var commandConfig = require('../command_config');

var command = commandConfig.pythonCommand + filePath;

exports.doTextAnalyze = function(req,res){

    if(!req.body.text){

        res.send({
            code:'400',
            msg:"参数无效 请重试"
        }).end();

        return;
    }

    var client = net.Socket();
    
    client.connect(8484, '127.0.0.1', function(){
        client.write(req.body.text);
    });

    client.on('data', function(data){
        var obj = JSON.parse(data)
        var classificationDict = {
            "study":"学习学术",
            "activity":"社团活动",
            "entrance":"招生考试",
            "social":"社会新闻"
        };
        var sentimentDict = {
            "1":"正面情感",
            "0":"中性情感",
            "-1":"负面情感"
        };
        resObj = {};
        resObj.sentiment = sentimentDict[obj.sentiment];
        resObj.classification = classificationDict[obj.classification];
        res.send({
            code:'200',
            result:resObj
        }).end();
    });
    
};