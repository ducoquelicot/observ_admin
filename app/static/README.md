# JavaScript prepopulate forms with URL parameters

## What does your script do?

My script prepopulates the 'subscribe' form with the output from the 'search' form. If you have performed a search with interesting results
and you want to subscribe to the query, you can press the 'subscribe' button and ideally, all you have to do is add the frequency and submit.

## How do you get the values?

In JS, you can use ```window.location.search.substring(1) ``` to get the URL from your current window. When you're processing queries, the
URL might look something like this: 

```
https://observ.news/search?q=police+AND+cats&doc_type=agenda&city=paloalto&submit=search
```

Using ```window.location.search.substring(1) ``` I will get the query substring, which is all this:

```
?q=police+AND+cats&doc_type=agenda&city=paloalto&submit=search
```

And then remove the ```?```by using ``` (1) ```

[click here for the SO explanation](https://stackoverflow.com/questions/14395090/location-search-in-javascript/14395123)

## How do you separate the values?

First, you split the string on the ```&``` so you have all the separate parameters. This can be done using 
```
var items = query.split("&");
```

I have created a function where I do all this work so that I can use the function to check the value for a certain key. 
To do that, you use a for loop to iterate over the variables and split them on the ```=``` so that you separate key and value.
After that, you check whether the key name for that variable matches the key you're looking for, and if so, return the value of that key. 

```
for (var i=0; i<items.length; i++) {
       var keys = items[i].split("=");
       if (keys[0] == key) {
           return keys[1];
    }
```

[click here for the example I used](https://css-tricks.com/snippets/javascript/get-url-variables/)

## How do you then prepopulate the form?

I store the output from the prepopulate function into new variables. For my specific use case, my query can contain multiple words. The
spaces will be turned into a '+' in the URL, but I don't want that + in my form, so I replaced the + in the query with a " ". In order
to do this with al the + in the query string, I made the replace function a global one. The finished code looks like this: 

```
var q = prepopulate("q")
var query = q.replace(/\+/g, " ")
var doctype = prepopulate("doc_type")
var cities = prepopulate("city")

document.getElementById("query").value = query;
document.getElementById("doctype").value = doctype;
document.getElementById("cities").value = cities
```

## Your code looks different though

I realized that although my code worked for a form where only one doctype and only one city was chosen, it didn't work when a user would
select multiple doctypes or cities. The url would look like this:

```
 /search?q=police&doc_type=agenda&doc_type=minutes&city=paloalto&submit=search
 
 ```
 
 And because the way my code was set up, I couldn't get the second doc_type in my variable. So, I need a way to store the variables in an
 object or arrray. Serdar helped me - unfortunately it's still not working, but I'm sure we'll get there at some point. 
 
 So far, I first created an object called data where I will store the arrays with the values for city and doctype. Then, I created a variable
 called 'multi' where I story the names of the keys that might have multiple values.
 
 ```
 var data = {city: [], doc_type: []};
 var multi = ["city", "doc_type"];
```

The for loop I created next will iterate over all the items in the 'items' variable and check whether the key part is similar to one of the 
values in the 'multi' variable. If so, it will append the value to the existing array. If not, it will just append the key/value pair to the object.

```
    for (var i=0; i<items.length; i++) {
        var keys = items[i].split("=")

        if (multi.includes(keys[0])) {
            data[keys[0]].push(keys[1])
        } else {
            data[keys[0]] = keys[1]
        }
    }
```

Then, I had to think about how I was going to get the values from the object. I stumbled upon [this](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty)
which enabled me to check whether the key existed in the object, and if so, return the value. 

```
    if (data.hasOwnProperty(key)) {
        return data[key];
    }
```

The rest of the code remains the same for now. The issue is that now, when I select multiple fields for doctype and/or city, the subscribe form
will throw an error as if I didn't select any option. I think this is due to the fact that WTForms, which I use to create my forms, stores the 
variables in a python list, and as such I need to feed the form a list of the options it's supposed to highlight.

## How much have you learned?

I think I am still in the process of learning, because it isn't quite working as planned yet. But overall, I think I understand quite well what I'm doing
and I would probably be able to explain to someone else what I did - I think I just tried to do that, so let me know if I succeeded. 
I am almost never able to code things from memory, which is why I have created a collection of SO answers and tutorials that I found useful in the past. 
I know I'm going to need them in the future, and that's fine. I also recycle a lot of code that I created earlier - I might not remember what I did, I am 
able to remember where I did a similar thing in the past once. 
