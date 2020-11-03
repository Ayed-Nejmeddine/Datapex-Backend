import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'hidePhone'
})
export class HidePhonePipe implements PipeTransform {

  transform(value: string, ...args: unknown[]): string {
    return value.replace(/.(?=.{2,}$)/g, '#');
  }

}
