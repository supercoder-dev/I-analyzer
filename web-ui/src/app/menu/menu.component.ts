import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { MenuItem } from 'primeng/primeng';
import { User } from '../models/index';
import { ConfigService, UserService } from '../services/index';

@Component({
    selector: 'menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.scss']
})
export class MenuComponent implements OnDestroy, OnInit {
    public currentUser: User | undefined;
    public isAdmin: boolean = false;
    public isGuest: boolean = true;

    private routerSubscription: Subscription;
    private menuItems: MenuItem[];

    constructor(private configService: ConfigService, private userService: UserService, private router: Router) {
        this.routerSubscription = router.events.subscribe(() => this.checkCurrentUser());
    }

    ngOnDestroy() {
        this.routerSubscription.unsubscribe();
    }

    ngOnInit() {
        this.checkCurrentUser();
    }

    public gotoAdmin() {
        this.configService.get().then(config => {
            window.location.href = config.adminUrl;
        });
    }

    public async logout() {
        let user = await this.userService.logout();
        this.currentUser = user;
    }

    public async login() {
        this.userService.showLogin(this.router.url);
    }

    private checkCurrentUser() {
        this.userService.getCurrentUser().catch(() => false).then(currentUser => {
            if (currentUser) {
                if (currentUser == this.currentUser) {
                    // nothing changed
                    return;
                }
                this.currentUser = currentUser as User;
                this.isAdmin = this.currentUser.hasRole('admin');
                this.isGuest = this.currentUser.hasRole('guest');
            } else {
                this.isAdmin = false;
                this.isGuest = true;
            }

            this.setMenuItems();
        });
    }

    private setMenuItems() {
        this.menuItems = [
            {
                label: 'Search history',
                icon: 'fa-history',
                command: (click) => {
                    this.router.navigate(['search-history'])
                }
            },
            ...this.isAdmin
                ? [
                    {
                        label: 'Administration',
                        icon: 'fa-cogs',
                        command: (click) => this.gotoAdmin(),
                    }] : [],
            this.isGuest
                ? {
                    label: 'Sign in',
                    icon: 'fa-sign-in',
                    command: (onclick) => this.login()
                } : {
                    label: 'Exit',
                    icon: 'fa-sign-out',
                    command: (onclick) => this.logout()
                }
        ];
    }
}
