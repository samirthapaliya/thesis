
    document.getElementById("id_rating").style.display="none";

    review_form = document.getElementsByClassName("review_form")[0]
    try {
        comment_editor = document.getElementsByClassName("comment_editor")[0]  
        comment_editor.style.display = "none"
    }
    catch(err) {
        
    }
    function show_form() {
            review_form.style.display = "block"
            comment_editor.style.display = "none"
    }
    function hide_form() {
            review_form.style.display = "none"
            comment_editor.style.display = "block"
    }


    for(let i = 0; i < parseInt(document.getElementById("id_rating").value); i++) {    
        document.getElementsByClassName("star_rate")[i].style.color = "#FF9529"; 
    }   
    prev_star_index = -1
    unrated = -1
    function rate(star_index) {
        if(unrated==0) {
            prev_star_index = -1
        }
        unrated = star_index+1  
        if(prev_star_index==star_index)  {
            unrated = 0
        }
        prev_star_index = star_index
        for(let i = 0; i <= star_index; i++) {    
            document.getElementsByClassName("star_rate")[i].style.color = "#FF9529"; 
        }   
        for(let i = unrated; i <= 4; i++) {    
            document.getElementsByClassName("star_rate")[i].style.color = "black"; 
        }
        document.getElementById("id_rating").value = unrated;
    }