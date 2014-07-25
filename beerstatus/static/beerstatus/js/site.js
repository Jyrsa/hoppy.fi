/*
Bootstrap that makes the front-end tick.
*/

var Alko = Backbone.Model.extend({
    defaults: {
        name: null,
        city: null,
        latitude: null,
        longitude: null,
        address: null,
        store_id: null,
        slug: null,
        id: null,
        store_url: null,
        gmaps_url: null,
    },
    initialize: function(){
        this.set("store_url",
                    "http://www.alko.fi/en/shops/"+this.get("store_id")+"/");
        this.set("gmaps_url",
            "https://www.google.com/maps/preview?q="+this.get("address"));
    }
});

var BeerAvailabilityWithRating = Backbone.Model.extend({
    defaults: {
        name: null,
        availability: null,
        date: null,
        ebu: null,
        abv: null,
        scores : null,
        price: null,
        volume: null,
        score : null, //just one score for now
        score_url : null, //just one score for now
        alko_url: null, //this must be constructed on the front-end as the
        //back-end is not locale aware
        },
    initialize: function(){
        this.set("alko_url" ,
                    "http://www.alko.fi/en/products/" +
                                this.get("alko_product_id") + "/"
                    )
    }
   })

var BeerView = Backbone.View.extend({
    tagName: "tr",
    initialize: function(params){
        params = params || {};
    },
    template: _.template('\
        <td><a href="<%= alko_url%>"><%= name %></a></td>\
        <td><a href="<%= score_url %>"><%= score %> pts</a></td>\
        <td><%= ebu %></td>\
        <td><%= abv %> %</td>\
        <td><%= volume %> l</td>\
        <td><%= price %> €</td>\
        <td><%= availability %></td>\
        <!--<td><%= date %></td>-->\
    '),
    render: function(){
        var class_ = ""
        if (this.model.get("availability") < 0){
            class_ = "danger";
        }
        else if (this.model.get("availability") > 0 &&
                this.model.get("availability") < 10){
            class_ = "warning";
        } else {
            class_ = "active";     
        }
        var json = this.model.toJSON();
        this.$el.html(this.template(json));
        if (this.model.get("availability") == 0){
            this.$el.addClass("hidden"); 
        }
        this.$el.addClass(class_);
        
        return this;
    }
})

var BeerCollection = Backbone.Collection.extend({
    model: BeerAvailabilityWithRating,
    url: function(){
            return "/api/v1/availability/?limit=0&location__slug=" +
            this.alko.get("slug");     
    },
    sortAttr: "score",
    legalSortAttrs: ["score", "abv", "ebu", "availability", "name",
                    "price", "volume", "date"],
    sortAsc: false,
    comparator: function(a_, b_){
        var a = a_.get(this.sortAttr),
            b = b_.get(this.sortAttr);
            if (a == b) return 0;
            if (this.sortAsc) return a > b? 1:-1;
            return a < b ? 1: -1;
        },
    setComparator: function(newcomp){
        if (this.legalSortAttrs.indexOf(newcomp) == -1)
            return
        if (newcomp == this.sortAttr)    
            this.sortAsc = !this.sortAsc;
        this.sortAttr = newcomp;
        this.sort();
    },
    initialize: function(params){
        this.locations = params.locations;
        this.router = params.router;
        if (this.locations && this.locations.selected){
            this.updateAlko(params.alko)
        }
        this.locations.on("alkochanged", this.updateAlko, this);
    },
    updateAlko: function(alko){
        this.alko = alko;
        this.fetch();
    },
    parse: function(response, options){
         var beers = [];
        _.each(response.objects, function(item, index, list){
            item.beer.score = item.beer.scores[0]["score"];
            item.beer.score_url = item.beer.scores[0]["url"];
            item.beer.availability = item.count;
            item.beer.date = item.date;
            item.abv = item.beer.abv;
            beers.push(new BeerAvailabilityWithRating(item.beer));
        });
        return beers;
    }
});

var BeerCollectionTable = Backbone.View.extend({
    el: "#beerTable",
    initialize: function(params){
        this.collection.on("fetch set reset sort", 
                            this.render,
                            this);
        this.collection.on("all", this.log);
    },
    events: {
        "click th": "changeSort",
        
    },
    changeSort: function(event_, params){
        this.collection.setComparator($(event_.target).data("sort"));
    },
    log: function(name, params){
        console.log("event " + name + " params");
    },
    template : _.template('\
    <thead>\
    <th data-sort="name">name</th>\
    <th data-sort="score"><a href="http://wwww.ratebeer.com">Ratebeer</a> score</th>\
    <th data-sort="ebu"> ebu </td>\
    <th data-sort="abv"> abv </td>\
    <th data-sort="volume">volume</th>\
    <th data-sort="price">price</th>\
    <th data-sort="availability">in stock</th>\
    <!--th data-sort="date">date</th-->\
    </thead>\
    <tbody></tbody>\
    '),
    render: function(){
        this.$el.hide().
                empty().
                append(this.template()).
                addClass("table").
                addClass("center");
        _.each(this.collection.models, function(item, index, list){
            
            var item = new BeerView({model:item});
            $("#"+this.el.id + " > tbody:last").append(item.render().el);

            if (index +1 == list.length)
                this.$el.show();
        }, this);
        return this;
    }

});

var AlkoLocations = Backbone.Collection.extend({
    model: Alko,
    url :"/api/v1/alko/?limit=0",
    initialize: function(models, options){
        options = options || {};
        this.selected = options.selected ? options.selected : null;
        this.router = options.router;
        this.selected_hash = null;
        this.on("add", this.checkToSetSlug, this);
    },
    parse: function(response, options){
        var alkos = [];
        _.each(response.objects, function(item, index, list){
            alkos.push(new Alko(item));
        });

        return alkos;
    },
    setSelected: function(model){
        this.selected = model;
        //fire change_selected event
        //that the availabilitycollection should listen to
        this.trigger("alkochanged", model);
        this.router.navigate(model.get("slug"));
        return; 
    },
    setSelectedSlug: function(input){
        this.selected_hash = input; 
    },
    checkToSetSlug: function(){
        if (this.selected_hash){
            var model = this.findWhere({slug:
            this.selected_hash});
            if (model) {
                this.setSelected(model);
                this.selected_hash = null;
            }
        }     
    }
    
});


var SelectedAlkoView = Backbone.View.extend({
    el: "#alkoDetails",
    initialize: function(params){
        this.collection.on("alkochanged", this.updateAlkoData, this);
    },
    template: _.template('\
        <li><a href="<%= store_url %>"><%= name %></a></li> \
        <li><a href="<%= gmaps_url %>"><%= address %></a></li> \
    '),
    updateAlkoData: function(model){
        this.model = model;
        this.render();
    },
    render: function(){
        this.$el.hide()
                 .html(this.template(this.model.toJSON()))
                 .show();
        
    }
})

var AlkoSearchView = Backbone.View.extend({
    initialize: function(params){
        this.collection.on("fetch set reset add change",
                        this.render,
                        this)
        this.render();
    },
    el: "#inputLocation",
    changeAlko: function(event_, ui){
        this.collection.setSelected(this.collection.findWhere({name:
                                ui.item.label}));
    },
    events : {
        "autocompleteselect": "changeAlko", 
    },
    render : function(){
            var vals = this.collection.pluck("name");
            $("#inputLocation").autocomplete({
                        minLength: 0,
                        source: vals,
                        });
            },
});


var BeerStatusRouter = Backbone.Router.extend({
    initialize: function(){
        this.als = new AlkoLocations([], {router:this});
        this.als.fetch();
        this.alsView = new AlkoSearchView({collection: this.als});
        this.bc = new BeerCollection({locations:this.als, router: this});
        this.bcView = new BeerCollectionTable({collection: this.bc});
        this.selAlView = new SelectedAlkoView({collection: this.als});
    },
    routes : {
       "" : "home",
       "*path" : "getAlko" //ToDo: routes for checking on a particular alko
    },  
    home: function(){
    },
    getAlko: function(path){
        this.als.setSelectedSlug(path);
    }
    });
$(function(){
    var router = new BeerStatusRouter();
    Backbone.history.start()
});
