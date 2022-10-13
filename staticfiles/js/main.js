// GET Search form and page links
let searchForm = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page-link");

// Ensure Search form Exists
if (searchForm) {
    for (let i = 0; i < pageLinks.length; i++) {
        pageLinks[i].addEventListener("click", function (e) {
            e.preventDefault();

            // GET THE DATA ATTRIBUTE
            let page = this.dataset.page;

            // GET THE SEARCH FORM VALUE
            searchForm.innerHTML += `<input value=${page} name="page" hidden />`;

            // SUBMIT THE FORM
            searchForm.submit();
        });
    }
}
