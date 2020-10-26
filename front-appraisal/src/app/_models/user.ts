import { Profile } from './profile';

export class User {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    photo?: string;
    token: string;
    profile? : Profile;
}