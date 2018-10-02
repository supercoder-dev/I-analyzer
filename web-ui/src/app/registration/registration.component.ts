import { Component, OnInit, OnDestroy } from '@angular/core'; 
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '../services/user.service';
import {NgForm} from '@angular/Forms';

//https://code.tutsplus.com/tutorials/introduction-to-forms-in-angular-4-template-driven-forms--cms-29766

@Component({
  selector: 'ia-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit, OnDestroy {
  private returnUrl: string;
  //public firstname: string;
  //public lastname: string;
  //public email: string;
  //public password: string;
  public isLoading: boolean;
  public isWrong: boolean;
  private success:boolean;
  private error=false;
  private firstname_result;
  private lastname_result;
  private email_result;

  constructor(private userService: UserService, private activatedRoute: ActivatedRoute, private router: Router, private title: Title ) {
    this.title.setTitle('I-Analyzer');
    UserService.loginActivated = true;

  }

  ngOnInit() {
    
  }
  ngOnDestroy(){  
    UserService.loginActivated = false;
  }

  //op scherm in template object tonen: {{object | json}}



  register(signupForm:NgForm){

      this.userService.register(signupForm.value.firstname, signupForm.value.lastname, signupForm.value.email, signupForm.value.password).then(result => {
            
              if (!result) {
                this.success=false;
                this.error=true;
                console.log(this.error);
                      }
              else {
                  if(result.success) {
                      this.success=true;
                      this.firstname_result=result.firstname;
                      this.lastname_result=result.lastname;
                      this.email_result=result.email;
                      console.log(this.error);
                    }
                    else{
                      this.error=true;
                    }
              }
        });
      }




}
