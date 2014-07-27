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
    },
    getDistance: function(lat, lon){
        //this is really evil, map projection people gonna hate
        //todo: update to a better projection
        var earth_radius = 6371; //km
        var lat1 = this.toRadians(lat);
        var lat2 = this.toRadians(this.get("latitude"));
        var lat1 = this.toRadians(lon);
        var lat2 = this.toRadians(this.get("longitude"));
        
        var x = (lat1-lat2)*Math.cos((lon1+lon2)/2);
        var y = lon1-lon2;
        return Math.sqrt(x*x+y*y)*R;
    },
    toRadians: function(value){
        return value * Math.PI/180; 
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
        <td class="hidden-xs"><%= ebu %></td>\
        <td class="hidden-xs"><%= abv %> %</td>\
        <td class="hidden-xs"><%= volume %> l</td>\
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
    <th data-sort="score"><a href="http://www.ratebeer.com">Ratebeer</a> score</th>\
    <th data-sort="ebu" class="hidden-xs"> ebu </td>\
    <th data-sort="abv" class="hidden-xs"> abv </td>\
    <th data-sort="volume" class="hidden-xs">volume</th>\
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


var AlkoDetailsView = Backbone.View.extend({
    el: "#alkoDetails",
    initialize: function(params){
        this.collection.on("alkochanged", this.updateAlkoData, this);
    },
    template: _.template('\
        <div class="center">\
        <span class="col-md-2 col-md-offset-4 col-xs-6"><a class="btn btn-default" href="<%= store_url %>">\
        store home page</a></span><span class="col-md-2 col-xs-6"> <a class="btn btn-default" href="<%= gmaps_url %>">\
        address in gmaps </a></div> \
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
    el: "#inputLocation",
    initialize: function(params){
        this.collection.on("sync", //sync is all we need for now
                                    //no need to trigger at each add
                        this.updateBloodHound,
                        this)
        params.alkolocations.on("alkochanged", this.setAlko, this);
        this.engine = new Bloodhound({
          name: 'alkos',
          local: [],
          datumTokenizer: function(d) {
            return Bloodhound.tokenizers.whitespace(d.get("name"));
          },
          queryTokenizer: Bloodhound.tokenizers.whitespace
        });
        this.engine.initialize();
        this.render();
        $(this.el).typeahead({
                        minLength: 0,
                        hilight: true,
                        }, {
                            source: this.engine.ttAdapter(),
                            displayKey: function(d){
                                return d.get("name");
                            }
            });
    },
    changeAlko: function(event_, suggestion, dataset){
        this.collection.setSelected(suggestion);
    },
    updateBloodHound: function(){
        this.engine.clear();
        this.engine.add(this.collection.models);
        this.engine.initialize(true);
    },
    setAlko: function(model){
        this.setText(model.get("name"));
    },
    setText: function(text){
        this.$el.val(text);   
    },
    clearText: function(event_, ui){
        this.setText("");
    },
    events : {
        "typeahead:selected": "changeAlko", 
        "click": "clearText"
    },
    render : function(){
    }
        
});


var BeerStatusRouter = Backbone.Router.extend({
    initialize: function(){
        this.als = new AlkoLocations([], {router:this});
        this.als.fetch();
        this.alsView = new AlkoSearchView({collection: this.als,
                        alkolocations: this.als});
        this.bc = new BeerCollection({locations:this.als, router: this});
        this.bcView = new BeerCollectionTable({collection: this.bc});
        this.selAlView = new AlkoDetailsView({collection: this.als});
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
