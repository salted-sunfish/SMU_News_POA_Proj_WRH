

var mongoose = require('mongoose');
var newsModel = require('../js_models/news');
var influenceModel = require('../js_models/influence');





var mediaSentimentRank = function(req,res){

    var query = {};
    var limit = req.query.limit || 5;
    query.sentiment = req.query.sentiment || "1";
    query.Uname = req.query.Uname || "上海海事大学";
    query.Uname = decodeURI(query.Uname);
    limit = parseInt(limit);


    // if(decodeURI(req.query.uname))
    //     query.Uname = decodeURI(req.query.uname);
    // else query.Uname = "上海海事大学";

    //console.log(query);
    // 聚合分组查询
    newsModel.aggregate(
        [
            {$match : query},
            //{$match : {Uname:"上海海事大学",sentiment:"0"}},
            //{$match : {sentiment:"-1"}},
            {$group:{ _id: '$media', total: { $sum: 1 }}},
            {$sort:{total:-1}},
            {$limit:limit}
        ],
        function (err, result) {
            if (err){
                console.log(err);
                res.send([]).end();
            }
            res.send(result).end();
        }
    );

};


function compare(property){
    return function(a,b){
        var value1 = a[property];
        var value2 = b[property];
        return value2 - value1;
    }
}


var mediaInfluence_mapreduce = function(req,res){

    var query = {};
    var limit = req.query.limit || 6;
    query.sentiment = req.query.sentiment || "1";
    query.Uname = req.query.uname || "上海海事大学";
    query.Uname = decodeURI(query.Uname);
    limit = parseInt(limit);
    console.log(limit);

    var mapReductOption = {};

    mapReductOption.query = query;
    mapReductOption.map = function(){
        emit(this.media,parseInt(this.ranking));
    };

    mapReductOption.reduce = function(key,values){
        // console.log(key);
        //console.log(values);

        var sum = 0;

        for(var i = 0; i <values.length;i++){
            var numValue = values[i];
            sum = sum + 1/(1+(numValue/1000))
        }
        return sum;
    };

    newsModel.mapReduce(mapReductOption,function(err,results){
        if (err){
            console.log(err);
            res.send([]).end();
        }
        results = results.sort(compare('value'));
        // var map_result_list = [];
        // if(limit <= results.length){
        //     for(var i = 0; i < limit;i++){
        //         map_result_list.push(results[i])
        //     }
        //     res.send(map_result_list).end();
        //     return;
        //
        // }else res.send(results).end();

        res.send(results).end();

    })
};


var mediaInfluence = function(req,res){

    var query = {};
    var limit = req.query.limit || 5;
    //query.sentiment = req.query.sentiment || "1";
    query.Uname = req.query.Uname || "上海海事大学";
    query.Uname = decodeURI(query.Uname);

    limit = parseInt(limit);
    console.log(limit);


    influenceModel.find(query,null,{sort:{"score":-1},limit:limit},function(err,results){
        if (err){
            console.log(err);
            res.send([]).end();
        }

        res.send(results).end();

    })

};


// 返回媒体及其含有的新闻个数(筛选,新闻数量需>10)
var medias = function(req, res){

    // var limit = req.query.limit || 100;
    // limit = parseInt(limit);

    newsModel.aggregate(
        [
            {$group: {_id: '$media', total: {$sum: 1}}},
            {$sort: {total: -1}},
            // {$limit: limit}
        ],
        function(err, result) {
            if (err){
                console.log(err);
                res.send([]).end();
            }
            result = result.filter(function(obj){
                return obj.total > 10;
            })
            res.send(result).end();
        }
    );
}


var universityRankOfOneMedia = function(req, res){
    var query = {}
    var limit;
    query.media = req.query.media || "网易";
    if (req.query.sentiment){
        query.sentiment = String(req.query.sentiment);
    }
    if (req.query.Uname){
        query.Uname = req.query.Uname;
    }
    limit = req.query.limit || 5;
    limit = parseInt(limit);

    newsModel.aggregate(
        [
            {$match: query},
            {$group: {_id: "$Uname", total: {$sum: 1}}},
            {$sort: {total: -1}},
            {$limit: limit},
        ],
        function(err, result) {
            if (err){
                console.log(err);
                res.send([]).end();
            }
            res.send(result).end();
        }
    )
}


module.exports = {
    mediaSentimentRank: mediaSentimentRank,
    mediaInfluence: mediaInfluence,
    medias: medias,
    universityRankOfOneMedia: universityRankOfOneMedia,
};