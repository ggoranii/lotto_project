from django import forms


class ManualLottoForm(forms.Form):
    """수동 번호 입력 폼"""
    
    num1 = forms.IntegerField(min_value=1, max_value=45, label='번호 1')
    num2 = forms.IntegerField(min_value=1, max_value=45, label='번호 2')
    num3 = forms.IntegerField(min_value=1, max_value=45, label='번호 3')
    num4 = forms.IntegerField(min_value=1, max_value=45, label='번호 4')
    num5 = forms.IntegerField(min_value=1, max_value=45, label='번호 5')
    num6 = forms.IntegerField(min_value=1, max_value=45, label='번호 6')

    def clean(self):
        """폼 전체 검증 - 중복 체크"""
        cleaned_data = super().clean()
        numbers = [
            cleaned_data.get(f'num{i}') for i in range(1, 7)
        ]
        
        # None이 있으면 (개별 필드 에러 있음) 추가 검증 안 함
        if None in numbers:
            return cleaned_data
        
        # 중복 체크
        if len(set(numbers)) != 6:
            raise forms.ValidationError("중복된 숫자가 있습니다. 서로 다른 6개의 숫자를 선택해주세요.")
        
        return cleaned_data
    
    def get_numbers(self):
        """입력된 6개 번호를 리스트로 반환"""
        return [self.cleaned_data[f'num{i}'] for i in range(1, 7)]