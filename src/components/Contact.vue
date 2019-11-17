<template>
    <section class="container mt-3">
        <h1>Contact</h1>

        <p>The MealsCount team is interested in getting feedback from interested parties. Please help us direct your inquiry 
            by filling out this form.</p>

        <form>
          <div class="form-group">
            <label for="exampleFormControlInput1">Email address</label>
            <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
          </div>
          <div class="form-group">
            <label for="exampleFormControlSelect1">My Background</label>
            <select name="background" class="form-control" id="exampleFormControlSelect1">
              <option>District / School Administrator</option>
              <option>Nutrition Director</option>
              <option>Food Policy Advocate</option>
              <option>Civic Tech / Softare Developer</option>
              <option>Parent / PTA</option>
              <option>Federal Government</option>
              <option>Press</option>
              <option>Other</option>
            </select>
          </div>
          <div class="form-group">
            <label for="exampleFormControlTextarea1">Questions / Comments / Concerns</label>
            <textarea class="form-control" id="exampleFormControlTextarea1" rows="5"></textarea>
          </div>
          <div class="form-group">
              <p>Sorry, we are not ready for feedback! Please contact us through our partner sites at this time.</p>
              <input type="submit" disabled value="Submit" />
          </div>
        </form>
    </section>
</template>